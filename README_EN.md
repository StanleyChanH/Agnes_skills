# 🎨 Agnes Media Skill

**English** | **[中文](README.md)**

> 🆓 **100% FREE** — Agnes AI image and video generation APIs are currently **zero cost**!

A Claude Code Skill for generating images and videos via the [Agnes AI](https://agnes-ai.com) API. Supports text-to-image, image-to-image, text-to-video, image-to-video, multi-image video, and keyframe animation.

## ✨ Features

### 🖼️ Image Generation (agnes-image-2.1-flash)
- **Text-to-Image** — Generate high-quality images from text descriptions
- **Image-to-Image** — Style transfer, scene transformation on existing images
- Custom sizes (1024x768, 768x1024, 1024x1024, etc.)
- URL or Base64 output

### 🎬 Video Generation (agnes-video-v2.0)
- **Text-to-Video** — Generate cinematic videos from text descriptions
- **Image-to-Video** — Animate static images into dynamic videos
- **Multi-Image Video** — Use multiple reference images to guide generation
- **Keyframe Animation** — Smooth transitions between keyframes
- Duration control (3s ~ 18s), resolution and frame rate customization
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
# Text-to-Image
python agnes-media/scripts/agnes_media.py image \
  --prompt "A luminous floating city above a misty canyon at sunrise, cinematic realism" \
  --size 1024x768 \
  --output output.png

# Image-to-Image
python agnes-media/scripts/agnes_media.py image \
  --prompt "Transform the scene into a rain-soaked cyberpunk night, preserve original composition" \
  --size 1024x768 \
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
- [Agnes Image 2.1 Flash Docs](https://agnes-ai.com/doc/agnes-image-21-flash)
- [Agnes Video V2.0 Docs](https://agnes-ai.com/doc/agnes-video-v20)
