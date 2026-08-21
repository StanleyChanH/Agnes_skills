# 🎨 Agnes Media Skill

**English** | **[中文](README.md)**

> 🆓 **100% FREE** — Agnes AI image and video generation APIs are currently **zero cost**!

A Claude Code Skill for generating images and videos via the [Agnes AI](https://agnes-ai.com) API. Supports text-to-image, image-to-image, text-to-video, image-to-video, multi-image video, and keyframe animation.

## ✨ Features

### 🖼️ Image Generation (agnes-image-2.1-flash)
- **Text-to-Image** — Generate high-quality images from text descriptions
- **Image-to-Image** — Style transfer, scene transformation on existing images
- **Multi-Image Composition** — Combine multiple reference images into a new one
- Tier-based sizes (`1K`/`2K`/`3K`/`4K`) + aspect ratios (8 options incl. `16:9`, `9:16`, `1:1`); exact sizes (multiples of 16) also supported
- URL or Base64 output

### 🎬 Video Generation (agnes-video-v2.0)
- **Text-to-Video** — Generate cinematic videos from text descriptions
- **Image-to-Video** — Animate static images into dynamic videos
- **Multi-Image Video** — Use multiple reference images to guide generation
- **Keyframe Animation** — Smooth transitions between keyframes
- Duration control (3s ~ 18s), resolution and frame rate customization
- Automatic size normalization (480p/720p/1080p tiers); actual output size reported on completion
- Async task processing with automatic progress polling

## 💰 Pricing

| Service | Regular Price | Current Price |
|---------|--------------|---------------|
| Image Generation | ~~$0.003/image~~ | **🆓 $0** |
| Video Generation | ~~$0.005/second~~ | **🆓 $0** |

> Sign up at https://agnes-ai.com to get a free API Key.

## 🚀 Quick Start

### 1. Get API Key

Sign up at https://agnes-ai.com and get your API Key.

### 2. Set Environment Variable

```bash
export AGNES_API_KEY="your-api-key-here"
```

### 3. Generate Images

```bash
# Text-to-Image (recommended: tier + ratio)
python agnes-media/scripts/agnes_media.py image \
  --prompt "A luminous floating city above a misty canyon at sunrise, cinematic realism" \
  --size 2K --ratio 16:9 \
  --output output.png

# Text-to-Image (legacy exact size, must be multiples of 16)
python agnes-media/scripts/agnes_media.py image \
  --prompt "A luminous floating city above a misty canyon at sunrise, cinematic realism" \
  --size 1024x768 \
  --output output.png

# Image-to-Image
python agnes-media/scripts/agnes_media.py image \
  --prompt "Transform the scene into a rain-soaked cyberpunk night, preserve original composition" \
  --size 2K --ratio 16:9 \
  --image-url "https://example.com/input.png" \
  --output transformed.png
```

### 4. Generate Videos

```bash
# Text-to-Video (~5 seconds)
python agnes-media/scripts/agnes_media.py video \
  --prompt "A cinematic shot of a cat walking on the beach at sunset, soft ocean waves, warm golden lighting" \
  --width 1152 --height 768 \
  --num-frames 121 --frame-rate 24 \
  --output video.mp4

# Image-to-Video
python agnes-media/scripts/agnes_media.py video \
  --prompt "The character slowly turns around to face the camera, natural expression, cinematic camera movement" \
  --image-url "https://example.com/character.png" \
  --output animated.mp4

# Keyframe Animation
python agnes-media/scripts/agnes_media.py video \
  --prompt "Smooth transition between two scenes" \
  --mode keyframes \
  --extra-images "https://example.com/kf1.png" "https://example.com/kf2.png" \
  --output transition.mp4
```

## 📐 Video Duration Reference

| Target Duration | num_frames | frame_rate |
|----------------|-----------|------------|
| ~3 sec | 81 | 24 |
| ~5 sec | 121 | 24 |
| ~10 sec | 241 | 24 |
| ~18 sec | 441 | 24 |

> `num_frames` must follow the `8n + 1` rule, with a maximum of 441.

## 🖼️ Image Size Reference

| Ratio | 1K | 2K | 3K | 4K |
|-------|----|----|----|----|
| `1:1` | 1024x1024 | 2048x2048 | 3072x3072 | 4096x4096 |
| `16:9` | 1312x736 | 2624x1472 | 3936x2208 | 5248x2944 |
| `9:16` | 736x1312 | 1472x2624 | 2208x3936 | 2944x5248 |
| `4:3` | 1152x864 | 2304x1728 | 3456x2592 | 4608x3456 |
| `3:4` | 864x1152 | 1728x2304 | 2592x3456 | 3456x4608 |

> Full table (incl. `2:3`, `3:2`, `21:9`) in the [API reference](agnes-media/references/api_reference.md). Note: `1920x1080` and `2560x1440` are NOT native output sizes — use `--size 2K --ratio 16:9` instead.

## 📹 Video Size Note

The video service auto-normalizes requested `width`/`height` to the nearest preset (`480p`/`720p`/`1080p` at `16:9`, `9:16`, `1:1`, `4:3`, `3:4`), so the actual output size may differ from the request. The script reports the actual output size and any normalization note on completion; trust `size`, `seconds`, and `metadata.size_mapping` in the API response when debugging.

## 📁 Project Structure

```
agnes-media/
├── SKILL.md                        # Skill main file (triggers + usage guide)
├── scripts/
│   └── agnes_media.py              # Core Python script
└── references/
    └── api_reference.md            # Full API reference documentation
```

## 🔧 Using as a Claude Code Skill

Place the `agnes-media` folder into your skill directory. Claude Code will automatically detect it and invoke it when you request image/video generation.

Install the packaged skill:
```
agnes-media.skill
```

## 📝 Prompt Tips

**Image prompt structure**:
```
[Subject] + [Scene / Environment] + [Style] + [Lighting] + [Composition] + [Quality]
```

**Video prompt structure**:
```
[Subject] + [Action] + [Scene] + [Camera Movement] + [Lighting] + [Style]
```

**For image-to-image / video**: Always describe both what to change and what to preserve (e.g., "Transform the scene into cyberpunk style while preserving the original composition").

## 📄 License

MIT License

## 🔗 Links

- [Agnes AI Official](https://agnes-ai.com)
- [Official Docs Index (llms.txt)](https://wiki.agnes-ai.com/llms.txt)
- [Agnes Image 2.1 Flash Docs](https://wiki.agnes-ai.com/en/docs/agnes-image-21-flash.md)
- [Agnes Video V2.0 Docs](https://wiki.agnes-ai.com/en/docs/agnes-video-v20.md)
- [API Common Error Codes](https://wiki.agnes-ai.com/en/docs/code.md)
