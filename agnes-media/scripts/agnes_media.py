#!/usr/bin/env python3
"""Agnes AI Media Generation Client.

Supports:
  - Text-to-Image / Image-to-Image (agnes-image-2.1-flash)
  - Text-to-Video / Image-to-Video / Multi-Image Video / Keyframe Animation (agnes-video-v2.0)

Requires: AGNES_API_KEY environment variable.
Usage:
  python agnes_media.py image --prompt "..." --size 1024x768 [--image-url URL] [--output path.png]
  python agnes_media.py video --prompt "..." [--image-url URL] [--width 1152] [--height 768] [--num-frames 121] [--frame-rate 24] [--output path.mp4]
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE_URL = "https://apihub.agnes-ai.com"
IMAGE_ENDPOINT = f"{BASE_URL}/v1/images/generations"
VIDEO_CREATE_ENDPOINT = f"{BASE_URL}/v1/videos"
VIDEO_RETRIEVE_BY_VIDEO_ID = f"{BASE_URL}/agnesapi"
VIDEO_RETRIEVE_BY_TASK_ID = f"{BASE_URL}/v1/videos"

IMAGE_MODEL = "agnes-image-2.1-flash"
VIDEO_MODEL = "agnes-video-v2.0"

DEFAULT_TIMEOUT = 300  # seconds for HTTP requests
POLL_INTERVAL = 5      # seconds between video status polls
MAX_POLL_TIME = 600     # max seconds to wait for video completion


def get_api_key():
    key = os.environ.get("AGNES_API_KEY")
    if not key:
        print("ERROR: AGNES_API_KEY environment variable not set.", file=sys.stderr)
        print("Get your API key from https://agnes-ai.com and set:", file=sys.stderr)
        print('  export AGNES_API_KEY="your-key-here"', file=sys.stderr)
        sys.exit(1)
    return key


def http_request(url, method="GET", headers=None, data=None, timeout=DEFAULT_TIMEOUT):
    """Make HTTP request and return parsed JSON response."""
    if headers is None:
        headers = {}
    headers["Content-Type"] = "application/json"

    req_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP Error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def parse_size(size_str):
    """Parse size string like '1024x768' into (width, height)."""
    try:
        parts = size_str.lower().split("x")
        return int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        print(f"ERROR: Invalid size format '{size_str}'. Use WIDTHxHEIGHT (e.g. 1024x768).", file=sys.stderr)
        sys.exit(1)


# ── Image Generation ──────────────────────────────────────────────────────────

def generate_image(api_key, prompt, size="1024x768", image_urls=None,
                   output_format="url", output_path=None):
    """Generate an image using Agnes Image 2.1 Flash.

    Args:
        api_key: API authentication key.
        prompt: Text prompt for generation.
        size: Output size string (e.g. "1024x768").
        image_urls: Optional list of image URLs for image-to-image.
        output_format: "url" or "base64".
        output_path: Optional local file path to save the image.
    """
    headers = {"Authorization": f"Bearer {api_key}"}

    body = {
        "model": IMAGE_MODEL,
        "prompt": prompt,
        "size": size,
    }

    # Image-to-image: put images inside extra_body
    if image_urls:
        body["extra_body"] = {
            "image": image_urls,
            "response_format": output_format,
        }
    else:
        # Text-to-image
        if output_format == "base64":
            body["return_base64"] = True
        else:
            body["extra_body"] = {"response_format": "url"}

    print(f"Generating image (model={IMAGE_MODEL}, size={size})...")
    if image_urls:
        print(f"  Mode: image-to-image ({len(image_urls)} input image(s))")
    else:
        print(f"  Mode: text-to-image")

    result = http_request(IMAGE_ENDPOINT, method="POST", headers=headers, data=body)

    if not result.get("data"):
        print("ERROR: No data in response.", file=sys.stderr)
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)

    item = result["data"][0]
    image_url = item.get("url")
    b64_data = item.get("b64_json")

    if b64_data:
        if output_path:
            save_base64_to_file(b64_data, output_path)
            print(f"Image saved to: {output_path}")
        else:
            print(f"Base64 image generated ({len(b64_data)} chars)")
            return {"format": "base64", "data": b64_data, "raw_response": result}
    elif image_url:
        if output_path:
            download_file(image_url, output_path)
            print(f"Image downloaded to: {output_path}")
        else:
            print(f"Image URL: {image_url}")
        return {"format": "url", "url": image_url, "raw_response": result}
    else:
        print("ERROR: No image URL or base64 data in response.", file=sys.stderr)
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)


# ── Video Generation ──────────────────────────────────────────────────────────

def create_video_task(api_key, prompt, image_url=None, extra_images=None,
                      mode=None, width=1152, height=768,
                      num_frames=121, frame_rate=24, seed=None,
                      negative_prompt=None):
    """Create a video generation task. Returns the task creation response."""
    headers = {"Authorization": f"Bearer {api_key}"}

    body = {
        "model": VIDEO_MODEL,
        "prompt": prompt,
    }

    if image_url:
        body["image"] = image_url

    if width:
        body["width"] = width
    if height:
        body["height"] = height
    if num_frames:
        body["num_frames"] = num_frames
    if frame_rate:
        body["frame_rate"] = frame_rate
    if seed is not None:
        body["seed"] = seed
    if negative_prompt:
        body["negative_prompt"] = negative_prompt

    # Multi-image or keyframe mode: use extra_body
    if extra_images or mode == "keyframes":
        extra = {}
        if extra_images:
            extra["image"] = extra_images
        if mode:
            extra["mode"] = mode
        body["extra_body"] = extra

    task_type = "text-to-video"
    if mode == "keyframes":
        task_type = "keyframe-animation"
    elif extra_images and len(extra_images) > 1:
        task_type = "multi-image-video"
    elif image_url:
        task_type = "image-to-video"

    print(f"Creating video task (model={VIDEO_MODEL}, {task_type})...")
    print(f"  Size: {width}x{height}, Frames: {num_frames}, FPS: {frame_rate}")
    duration = num_frames / frame_rate if frame_rate else 0
    print(f"  Estimated duration: ~{duration:.1f}s")

    return http_request(VIDEO_CREATE_ENDPOINT, method="POST", headers=headers, data=body)


def poll_video_result(api_key, video_id=None, task_id=None):
    """Poll until video generation completes. Returns final result."""
    headers = {"Authorization": f"Bearer {api_key}"}

    if video_id:
        poll_url = f"{VIDEO_RETRIEVE_BY_VIDEO_ID}?video_id={video_id}"
    elif task_id:
        poll_url = f"{VIDEO_RETRIEVE_BY_TASK_ID}/{task_id}"
    else:
        print("ERROR: Need video_id or task_id to poll.", file=sys.stderr)
        sys.exit(1)

    start_time = time.time()
    last_progress = -1

    while True:
        elapsed = time.time() - start_time
        if elapsed > MAX_POLL_TIME:
            print(f"\nERROR: Timed out after {MAX_POLL_TIME}s.", file=sys.stderr)
            sys.exit(1)

        result = http_request(poll_url, method="GET", headers=headers)
        status = result.get("status", "unknown")
        progress = result.get("progress", 0)

        if progress != last_progress:
            bar_len = 30
            filled = int(bar_len * progress / 100)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"\r  [{bar}] {progress}% — {status}", end="", flush=True)
            last_progress = progress

        if status == "completed":
            print()  # newline after progress bar
            return result
        elif status == "failed":
            print()
            print("ERROR: Video generation failed.", file=sys.stderr)
            print(json.dumps(result, indent=2), file=sys.stderr)
            sys.exit(1)

        time.sleep(POLL_INTERVAL)


def generate_video(api_key, prompt, image_url=None, extra_images=None,
                   mode=None, width=1152, height=768,
                   num_frames=121, frame_rate=24, seed=None,
                   negative_prompt=None, output_path=None):
    """Full video generation workflow: create task, poll, save result."""
    # Create task
    task = create_video_task(
        api_key, prompt, image_url=image_url, extra_images=extra_images,
        mode=mode, width=width, height=height,
        num_frames=num_frames, frame_rate=frame_rate, seed=seed,
        negative_prompt=negative_prompt,
    )

    video_id = task.get("video_id")
    task_id = task.get("task_id") or task.get("id")
    print(f"  Task created: video_id={video_id}, task_id={task_id}")

    # Poll for result
    result = poll_video_result(api_key, video_id=video_id, task_id=task_id)

    video_url = result.get("remixed_from_video_id")
    if not video_url:
        print("ERROR: Video completed but no URL found.", file=sys.stderr)
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)

    print(f"Video URL: {video_url}")

    # Save if requested
    if output_path:
        download_file(video_url, output_path)
        print(f"Video downloaded to: {output_path}")

    return {"url": video_url, "raw_response": result}


# ── Utilities ─────────────────────────────────────────────────────────────────

def download_file(url, path):
    """Download a file from URL to local path."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    urllib.request.urlretrieve(url, path)


def save_base64_to_file(b64_data, path):
    """Save base64 data to a file."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64_data))


def file_to_data_uri(path):
    """Convert a local file to a data URI (for image-to-image Base64 input)."""
    ext = os.path.splitext(path)[1].lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".webp": "image/webp", ".gif": "image/gif"}
    mime = mime_map.get(ext, "image/png")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


# ── CLI ───────────────────────────────────────────────────────────────────────

def cmd_image(args):
    api_key = get_api_key()
    image_urls = []

    if args.image_url:
        image_urls.append(args.image_url)
    if args.image_file:
        image_urls.append(file_to_data_uri(args.image_file))

    generate_image(
        api_key, args.prompt, size=args.size,
        image_urls=image_urls or None,
        output_format=args.format,
        output_path=args.output,
    )


def cmd_video(args):
    api_key = get_api_key()

    extra_images = []
    if args.extra_images:
        extra_images = args.extra_images

    generate_video(
        api_key, args.prompt,
        image_url=args.image_url,
        extra_images=extra_images or None,
        mode=args.mode,
        width=args.width, height=args.height,
        num_frames=args.num_frames,
        frame_rate=args.frame_rate,
        seed=args.seed,
        negative_prompt=args.negative_prompt,
        output_path=args.output,
    )


def main():
    parser = argparse.ArgumentParser(description="Agnes AI Media Generation")
    sub = parser.add_subparsers(dest="command", required=True)

    # ── image subcommand ──
    img = sub.add_parser("image", help="Generate images with Agnes Image 2.1 Flash")
    img.add_argument("--prompt", required=True, help="Text prompt for image generation")
    img.add_argument("--size", default="1024x768", help="Output size (default: 1024x768)")
    img.add_argument("--image-url", help="Input image URL for image-to-image")
    img.add_argument("--image-file", help="Local image file path for image-to-image (converted to data URI)")
    img.add_argument("--format", choices=["url", "base64"], default="url",
                     help="Output format (default: url)")
    img.add_argument("--output", help="Save output to this file path")

    # ── video subcommand ──
    vid = sub.add_parser("video", help="Generate videos with Agnes Video V2.0")
    vid.add_argument("--prompt", required=True, help="Text prompt for video generation")
    vid.add_argument("--image-url", help="Input image URL for image-to-video")
    vid.add_argument("--extra-images", nargs="+", help="Additional image URLs for multi-image/keyframe mode")
    vid.add_argument("--mode", choices=["ti2vid", "keyframes"], help="Generation mode")
    vid.add_argument("--width", type=int, default=1152, help="Video width (default: 1152)")
    vid.add_argument("--height", type=int, default=768, help="Video height (default: 768)")
    vid.add_argument("--num-frames", type=int, default=121, help="Number of frames, must follow 8n+1 rule, max 441 (default: 121)")
    vid.add_argument("--frame-rate", type=int, default=24, help="FPS 1-60 (default: 24)")
    vid.add_argument("--seed", type=int, help="Random seed for reproducibility")
    vid.add_argument("--negative-prompt", help="Negative prompt to avoid unwanted content")
    vid.add_argument("--output", help="Save video to this file path")

    args = parser.parse_args()
    if args.command == "image":
        cmd_image(args)
    elif args.command == "video":
        cmd_video(args)


if __name__ == "__main__":
    main()
