# Agnes AI API Reference

> Official docs index: https://wiki.agnes-ai.com/llms.txt
> - Image model docs: https://wiki.agnes-ai.com/en/docs/agnes-image-21-flash.md
> - Video model docs: https://wiki.agnes-ai.com/en/docs/agnes-video-v20.md
> - Common error codes: https://wiki.agnes-ai.com/en/docs/code.md

## Authentication

All requests require Bearer token authentication:
```
Authorization: Bearer YOUR_API_KEY
```
Set the `AGNES_API_KEY` environment variable. Free tier is rate-limited to RPM 20.

---

## Image Generation (agnes-image-2.1-flash)

### Endpoint
```
POST https://apihub.agnes-ai.com/v1/images/generations
Content-Type: application/json
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Use `agnes-image-2.1-flash` |
| `prompt` | string | Yes | Text description for image generation |
| `size` | string | Yes | Output size tier: `1K`, `2K`, `3K`, `4K` (recommended). Legacy exact sizes like `1024x768` are accepted but may be normalized |
| `ratio` | string | No | Aspect ratio paired with tier sizes. `1:1`, `3:4`, `4:3`, `16:9`, `9:16`, `2:3`, `3:2`, `21:9`. Defaults to `1:1` |
| `return_base64` | boolean | No | For text-to-image Base64 output |
| `extra_body` | object | No | Advanced parameters container |
| `extra_body.response_format` | string | No | `"url"` or `"b64_json"` |
| `extra_body.image` | string[] | No | Input image URLs or Data URI for image-to-image / multi-image composition |

### Critical Rules
- **Never** put `response_format` at the top level — always inside `extra_body`
- **Never** use `tags: ["img2img"]` — not needed for image-to-image
- For text-to-image URL output: use `extra_body.response_format: "url"`
- For text-to-image Base64 output: use top-level `return_base64: true`
- For image-to-image URL output: use `extra_body.image` + `extra_body.response_format: "url"`
- For image-to-image Base64 output: use `extra_body.image` + `extra_body.response_format: "b64_json"`
- **Exact sizes must be multiples of 16** (e.g. `1024x768`), otherwise the request may fail with HTTP 500. Prefer tier-based sizes to avoid this entirely.
- `1920x1080` and `2560x1440` are NOT native output sizes — request `size: "2K"` + `ratio: "16:9"` instead, then crop/scale downstream.

### Output Size Reference

| Ratio | 1K | 2K | 3K | 4K |
|-------|----|----|----|----|
| `1:1` | 1024x1024 | 2048x2048 | 3072x3072 | 4096x4096 |
| `3:4` | 864x1152 | 1728x2304 | 2592x3456 | 3456x4608 |
| `4:3` | 1152x864 | 2304x1728 | 3456x2592 | 4608x3456 |
| `16:9` | 1312x736 | 2624x1472 | 3936x2208 | 5248x2944 |
| `9:16` | 736x1312 | 1472x2624 | 2208x3936 | 2944x5248 |
| `2:3` | 832x1248 | 1664x2496 | 2496x3744 | 3328x4992 |
| `3:2` | 1248x832 | 2496x1664 | 3744x2496 | 4992x3328 |
| `21:9` | 1568x672 | 3136x1344 | 4704x2016 | 6272x2688 |

### Response

**URL output:**
```json
{
  "created": 1780000000,
  "data": [{
    "url": "https://storage.googleapis.com/agnes-aigc/xxx.png",
    "b64_json": null,
    "revised_prompt": null
  }]
}
```

**Base64 output:**
```json
{
  "created": 1780000000,
  "data": [{
    "url": null,
    "b64_json": "iVBORw0KGgo...",
    "revised_prompt": null
  }]
}
```

### Examples

**Text-to-Image (tier size + ratio, recommended):**
```bash
curl https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "A cinematic product hero image for a desktop monitor wallpaper, clean lighting, high detail",
    "size": "2K",
    "ratio": "16:9",
    "extra_body": {"response_format": "url"}
  }'
```
Returns a 16:9 2K image at `2624x1472`.

**Text-to-Image (legacy exact size):**
```bash
curl https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "A luminous floating city above a misty canyon at sunrise, cinematic realism",
    "size": "1024x768",
    "extra_body": {"response_format": "url"}
  }'
```

**Image-to-Image (URL input → URL output):**
```bash
curl https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "Transform into cyberpunk night with neon reflections, preserve composition",
    "size": "2K",
    "ratio": "16:9",
    "extra_body": {
      "image": ["https://example.com/input.png"],
      "response_format": "url"
    }
  }'
```

**Image-to-Image (Data URI Base64 input):**
```bash
# Data URI format: data:image/png;base64,BASE64_HERE
curl https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "Make the object matte black, preserve composition",
    "size": "1K",
    "extra_body": {
      "image": ["data:image/png;base64,BASE64_HERE"],
      "response_format": "b64_json"
    }
  }'
```

### Prompt Best Practices

Structure: `[Subject] + [Scene / Environment] + [Style] + [Lighting] + [Composition] + [Quality]`

- Include: main subject, scene, visual style, lighting, camera angle, composition, detail level
- For image-to-image: specify what to change AND what to preserve
- For multi-image composition: state each reference image's role and how they combine

---

## Video Generation (agnes-video-v2.0)

### Async Workflow
1. **Create task** → get `video_id` and `task_id`
2. **Poll for result** using `video_id` (recommended) or `task_id`
3. **Get video URL** from `metadata.url` when `status` is `completed`

### Size Normalization

The service auto-normalizes `width`/`height` to the nearest standard preset. Three resolution tiers are supported: `480p`, `720p`, `1080p`, at these aspect ratios:

| Aspect ratio | Typical use |
|--------------|-------------|
| `16:9` | Landscape video, product demos, YouTube-style content |
| `9:16` | Vertical short video, TikTok / Reels / Shorts |
| `1:1` | Square video, social feeds |
| `4:3` | Classic landscape, presentations |
| `3:4` | Portrait presentations, product-focused content |

The requested size may therefore differ from the actual output (e.g. `1024x576` → `832x448` at 480p/16:9). Always trust the `size`, `seconds`, and `metadata.size_mapping` fields in the API response over the request parameters.

### Create Task

```
POST https://apihub.agnes-ai.com/v1/videos
Content-Type: application/json
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Use `agnes-video-v2.0` |
| `prompt` | string | Yes | Text description of video content |
| `image` | string | No | Single image URL for image-to-video |
| `mode` | string | No | `ti2vid` or `keyframes` |
| `height` | integer | No | Video height (default: 768). Must be a multiple of 64; will be normalized to the nearest preset |
| `width` | integer | No | Video width (default: 1152). Must be a multiple of 64; will be normalized to the nearest preset |
| `num_frames` | integer | No | Total frames, ≤441, must follow 8n+1 rule |
| `frame_rate` | number | No | FPS, range 1–60 |
| `num_inference_steps` | integer | No | Inference steps |
| `seed` | integer | No | Random seed for reproducibility |
| `negative_prompt` | string | No | Content to avoid |
| `extra_body.image` | string[] | No | Image URLs for multi-image / keyframe |
| `extra_body.mode` | string | No | Mode setting, e.g. `"keyframes"` |

#### num_frames Rule
- Must be ≤ 441
- Must follow `8n + 1` rule: 81, 121, 161, 201, 241, 281, 321, 361, 401, 441

#### Common Duration Presets

| Duration | num_frames | frame_rate |
|----------|-----------|------------|
| ~3s | 81 | 24 |
| ~5s | 121 | 24 |
| ~10s | 241 | 24 |
| ~18s | 441 | 24 |

#### Create Response
```json
{
  "id": "task_YOUR_TASK_ID",
  "task_id": "task_YOUR_TASK_ID",
  "video_id": "video_YOUR_VIDEO_ID",
  "object": "video",
  "model": "agnes-video-v2.0",
  "status": "queued",
  "progress": 0,
  "created_at": 1780457477,
  "seconds": "10.0",
  "size": "1280x768"
}
```

### Retrieve Result

**Recommended (by video_id):**
```
GET https://apihub.agnes-ai.com/agnesapi?video_id={video_id}
GET https://apihub.agnes-ai.com/agnesapi?video_id={video_id}&model_name=agnes-video-v2.0
```
The `model_name` query parameter is for upstream raw video IDs or non-default models.

**Legacy (by task_id):**
```
GET https://apihub.agnes-ai.com/v1/videos/{task_id}
```

#### Task Statuses
| Status | Description |
|--------|-------------|
| `queued` | Waiting in queue |
| `in_progress` | Video being generated |
| `completed` | Successfully generated |
| `failed` | Generation failed |

#### Completed Response
```json
{
  "id": "task_YOUR_TASK_ID",
  "video_id": "task_YOUR_TASK_ID",
  "task_id": "task_YOUR_TASK_ID",
  "object": "video",
  "model": "agnes-video-v2.0",
  "status": "completed",
  "progress": 100,
  "created_at": 1784530473,
  "completed_at": 1784530510,
  "seconds": "1.0",
  "size": "832x448",
  "metadata": {
    "size_mapping": {
      "adjusted": true,
      "height": 448,
      "message": "Input size 1024x576 was mapped to nearest preset 480p/16:9 (832x448)",
      "ratio": "16:9",
      "requested_height": 576,
      "requested_width": 1024,
      "resolution": "480p",
      "width": 832
    },
    "url": "https://platform-outputs.agnes-ai.space/videos/agnes-video-v2.0/task_YOUR_TASK_ID.mp4"
  }
}
```

**The final video URL is in `metadata.url`** — available only when `status` is `completed`.

Key response fields:
- `size` — the normalized actual output resolution (may differ from the request)
- `seconds` — actual video duration in seconds (string)
- `completed_at` — task completion timestamp
- `metadata.url` — final video download URL
- `metadata.size_mapping` — size normalization details: requested vs actual size, aspect ratio, resolution tier, and a human-readable `message` when `adjusted` is true
- `error` — error object on failure (may be absent on success)

### Examples

**Text-to-Video:**
```bash
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-v2.0",
    "prompt": "A cinematic shot of a cat walking on the beach at sunset",
    "height": 768, "width": 1152,
    "num_frames": 121, "frame_rate": 24
  }'
```

**Image-to-Video:**
```bash
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-v2.0",
    "prompt": "The woman slowly turns around, cinematic camera movement",
    "image": "https://example.com/image.png",
    "num_frames": 121, "frame_rate": 24
  }'
```

**Multi-Image Video:**
```bash
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-v2.0",
    "prompt": "Smooth transformation between two reference images",
    "extra_body": {
      "image": ["https://example.com/img1.png", "https://example.com/img2.png"]
    },
    "num_frames": 121, "frame_rate": 24
  }'
```

**Keyframe Animation:**
```bash
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-v2.0",
    "prompt": "Smooth cinematic transition between keyframes",
    "extra_body": {
      "image": ["https://example.com/kf1.png", "https://example.com/kf2.png"],
      "mode": "keyframes"
    },
    "num_frames": 121, "frame_rate": 24
  }'
```

### Prompt Best Practices

**Text-to-Video:** `[Subject] + [Action] + [Scene] + [Camera Movement] + [Lighting] + [Style]`

**Image-to-Video:** Describe what should move and what should remain stable.

**Keyframe:** Describe transition relationship between keyframes.

---

## Error Codes

Common codes (full list: https://wiki.agnes-ai.com/en/docs/code.md):

| Code | Description |
|------|-------------|
| 400 | Invalid request — check parameters, JSON format, video constraints (FPS/duration/resolution/ratio) |
| 401 | Unauthorized — check API key |
| 402 | Insufficient balance or quota |
| 403 | No permission to access the model/resource |
| 404 | Task, video, or path not found — check Base URL and model name |
| 405 | Request method not supported (GET vs POST) |
| 408 | Request timed out |
| 409 | Conflict — duplicate task submission |
| 413 | Request body too large — use a public image URL instead of huge base64 |
| 415 | Unsupported file format / Content-Type |
| 422 | Parameter values out of range (seed, resolution, ratio, FPS) or inaccessible image URL |
| 429 | Rate limited — free tier is RPM 20; wait and retry |
| 431 | Request headers too large |
| 499 | Client closed the connection early |
| 500 | Server error — image dimensions must be multiples of 16; video dimensions must be multiples of 64 |
| 502 | Bad gateway — network/DNS/proxy issue or upstream fluctuation |
| 503 | Service busy or model name incorrect — retry later |
| 504 | Gateway timeout — lower generation specs or retry |
| 520/522/524 | Network/upstream errors — retry, check proxy/DNS |

## Pricing

| Service | Regular price | Current price |
|---------|---------------|---------------|
| Image generation | $0.003 / image | $0 / image |
| Video duration | $0.005 / second | $0 / second |
