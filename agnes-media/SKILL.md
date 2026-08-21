---
name: agnes-media
description: Generate images and videos using the Agnes AI API (Sapiens AI). Supports text-to-image, image-to-image (agnes-image-2.1-flash), text-to-video, image-to-video, multi-image video, and keyframe animation (agnes-video-v2.0). Use when the user asks to generate AI images, create AI videos, animate images, or perform any visual media generation task with Agnes AI. Triggers on keywords like "generate image", "create video", "AI art", "text to image", "image to video", "animate image", "Agnes image", "Agnes video".
---

# Agnes Media Generator

Generate images and videos via the Agnes AI API.

## Prerequisites

Set the `AGNES_API_KEY` environment variable:
```bash
export AGNES_API_KEY="your-api-key-here"
```
Get an API key from https://agnes-ai.com.

## Workflow

1. **Detect intent** — determine if the user wants an image or video.
2. **Collect params** — prompt (required), size/dimensions, input images, output format.
3. **Run the script** — execute `scripts/agnes_media.py` with appropriate arguments.
4. **Deliver result** — show the URL or local file path to the user.

## Quick Reference

### Generate Image (Text-to-Image)

```bash
# Recommended: tier size + aspect ratio
python scripts/agnes_media.py image \
  --prompt "A luminous floating city above a misty canyon, cinematic realism" \
  --size 2K --ratio 16:9 \
  --output output.png

# Legacy: exact size (must be multiples of 16)
python scripts/agnes_media.py image \
  --prompt "A luminous floating city above a misty canyon, cinematic realism" \
  --size 1024x768 \
  --output output.png
```

### Generate Image (Image-to-Image)

```bash
python scripts/agnes_media.py image \
  --prompt "Transform into cyberpunk night with neon reflections, preserve composition" \
  --size 2K --ratio 16:9 \
  --image-url "https://example.com/input.png" \
  --output transformed.png
```

Use `--image-file` instead of `--image-url` to use a local file as input.

### Generate Video (Text-to-Video)

```bash
python scripts/agnes_media.py video \
  --prompt "A cinematic shot of a cat walking on the beach at sunset" \
  --width 1152 --height 768 \
  --num-frames 121 --frame-rate 24 \
  --output video.mp4
```

### Generate Video (Image-to-Video)

```bash
python scripts/agnes_media.py video \
  --prompt "The character turns around slowly, cinematic camera movement" \
  --image-url "https://example.com/character.png" \
  --num-frames 121 --frame-rate 24 \
  --output animated.mp4
```

### Generate Video (Multi-Image / Keyframe)

```bash
python scripts/agnes_media.py video \
  --prompt "Smooth transition between scenes" \
  --mode keyframes \
  --extra-images "https://example.com/img1.png" "https://example.com/img2.png" \
  --num-frames 121 --frame-rate 24 \
  --output transition.mp4
```

## Image Parameters

| Param | Default | Description |
|-------|---------|-------------|
| `--prompt` | required | Text prompt |
| `--size` | `1024x768` | Size tier `1K`/`2K`/`3K`/`4K` (recommended) or exact WIDTHxHEIGHT (multiples of 16) |
| `--ratio` | — | Aspect ratio with tier sizes: `1:1`, `3:4`, `4:3`, `16:9`, `9:16`, `2:3`, `3:2`, `21:9` |
| `--image-url` | — | Input image URL for img2img |
| `--image-file` | — | Local image file for img2img (auto-converts to data URI) |
| `--format` | `url` | `url` or `base64` |
| `--output` | — | Save to local file |

Common size combinations: `--size 2K --ratio 16:9` → 2624x1472; `--size 1K --ratio 1:1` → 1024x1024. Full size table in the [API reference](references/api_reference.md).

## Video Parameters

| Param | Default | Description |
|-------|---------|-------------|
| `--prompt` | required | Text prompt |
| `--image-url` | — | Input image for img2vid |
| `--extra-images` | — | Additional image URLs (multi-image / keyframe) |
| `--mode` | — | `ti2vid` or `keyframes` |
| `--width` | `1152` | Video width (multiple of 64; auto-normalized to nearest preset) |
| `--height` | `768` | Video height (multiple of 64; auto-normalized to nearest preset) |
| `--num-frames` | `121` | Frame count (8n+1 rule, max 441) |
| `--frame-rate` | `24` | FPS (1–60) |
| `--seed` | — | Reproducible seed |
| `--negative-prompt` | — | Content to avoid |
| `--output` | — | Save to local file |

**Size normalization**: the service maps `width`/`height` to the nearest standard preset (`480p`/`720p`/`1080p` at `16:9`, `9:16`, `1:1`, `4:3`, `3:4`), so the actual output size may differ from the request. The script reports the actual `size` and any normalization note when done.

## Video Duration Guide

| Duration | num_frames | frame_rate |
|----------|-----------|------------|
| ~3s | 81 | 24 |
| ~5s | 121 | 24 |
| ~10s | 241 | 24 |
| ~18s | 441 | 24 |

## Important API Rules

- **Image `response_format`**: NEVER put at request top level. Always inside `extra_body`.
- **Image-to-image**: Do NOT use `tags: ["img2img"]`. Just provide images in `extra_body.image`.
- **Video is async**: create task → poll with `video_id` → get URL from `metadata.url` (only present when `status` is `completed`).
- **Video frames**: `num_frames` must be ≤ 441 and follow 8n+1 rule.
- **Image exact sizes** must be multiples of 16 (tiers like `2K` avoid this). **Video dimensions** must be multiples of 64 and are auto-normalized to the nearest preset — trust `size`/`metadata.size_mapping` in the response.
- Prefer tier sizes (`1K`–`4K`) + `--ratio` for images; `1920x1080`/`2560x1440` are not native outputs (request `2K` + `16:9` instead).

## Prompt Tips

**Image prompts** — structure as: `[Subject] + [Scene] + [Style] + [Lighting] + [Composition] + [Quality]`

**Video prompts** — structure as: `[Subject] + [Action] + [Scene] + [Camera Movement] + [Lighting] + [Style]`

**Image-to-image**: always specify what to change AND what to preserve (e.g. "preserve original composition").

## API Reference

See [references/api_reference.md](references/api_reference.md) for full endpoint details, all parameters, raw curl examples, and error codes.
