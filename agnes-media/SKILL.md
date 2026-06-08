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
python scripts/agnes_media.py image \
  --prompt "A luminous floating city above a misty canyon, cinematic realism" \
  --size 1024x768 \
  --output output.png
```

### Generate Image (Image-to-Image)

```bash
python scripts/agnes_media.py image \
  --prompt "Transform into cyberpunk night with neon reflections, preserve composition" \
  --size 1024x768 \
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
| `--size` | `1024x768` | Output size (WIDTHxHEIGHT) |
| `--image-url` | — | Input image URL for img2img |
| `--image-file` | — | Local image file for img2img (auto-converts to data URI) |
| `--format` | `url` | `url` or `base64` |
| `--output` | — | Save to local file |

## Video Parameters

| Param | Default | Description |
|-------|---------|-------------|
| `--prompt` | required | Text prompt |
| `--image-url` | — | Input image for img2vid |
| `--extra-images` | — | Additional image URLs (multi-image / keyframe) |
| `--mode` | — | `ti2vid` or `keyframes` |
| `--width` | `1152` | Video width |
| `--height` | `768` | Video height |
| `--num-frames` | `121` | Frame count (8n+1 rule, max 441) |
| `--frame-rate` | `24` | FPS (1–60) |
| `--seed` | — | Reproducible seed |
| `--negative-prompt` | — | Content to avoid |
| `--output` | — | Save to local file |

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
- **Video is async**: create task → poll with `video_id` → get URL from `remixed_from_video_id`.
- **Video frames**: `num_frames` must be ≤ 441 and follow 8n+1 rule.

## Prompt Tips

**Image prompts** — structure as: `[Subject] + [Scene] + [Style] + [Lighting] + [Composition] + [Quality]`

**Video prompts** — structure as: `[Subject] + [Action] + [Scene] + [Camera Movement] + [Lighting] + [Style]`

**Image-to-image**: always specify what to change AND what to preserve (e.g. "preserve original composition").

## API Reference

See [references/api_reference.md](references/api_reference.md) for full endpoint details, all parameters, raw curl examples, and error codes.
