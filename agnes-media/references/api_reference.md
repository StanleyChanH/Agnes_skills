# Agnes AI API Reference

## Authentication

All requests require Bearer token authentication:
```
Authorization: Bearer YOUR_API_KEY
```
Set the `AGNES_API_KEY` environment variable.

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
| `size` | string | Yes | Output size, e.g. `1024x768`, `768x1024`, `1024x1024` |
| `return_base64` | boolean | No | For text-to-image Base64 output |
| `extra_body` | object | No | Advanced parameters container |
| `extra_body.response_format` | string | No | `"url"` or `"b64_json"` |
| `extra_body.image` | string[] | No | Input image URLs or Data URI for image-to-image |

### Critical Rules
- **Never** put `response_format` at the top level — always inside `extra_body`
- **Never** use `tags: ["img2img"]` — not needed for image-to-image
- For text-to-image URL output: use `extra_body.response_format: "url"`
- For text-to-image Base64 output: use top-level `return_base64: true`
- For image-to-image URL output: use `extra_body.image` + `extra_body.response_format: "url"`
- For image-to-image Base64 output: use `extra_body.image` + `extra_body.response_format: "b64_json"`

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

**Text-to-Image (URL output):**
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
    "size": "1024x768",
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
    "size": "1024x768",
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

---

## Video Generation (agnes-video-v2.0)

### Async Workflow
1. **Create task** → get `video_id` and `task_id`
2. **Poll for result** using `video_id` (recommended) or `task_id`
3. **Get video URL** from `remixed_from_video_id` when `status` is `completed`

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
| `height` | integer | No | Video height (default: 768) |
| `width` | integer | No | Video width (default: 1152) |
| `num_frames` | integer | No | Total frames, ≤441, must follow 8n+1 rule |
| `frame_rate` | integer | No | FPS, range 1–60 |
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
  "id": "task_xxx",
  "task_id": "task_xxx",
  "video_id": "video_xxx",
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
  "id": "task_xxx",
  "video_id": "video_xxx",
  "model": "agnes-video-v2.0",
  "object": "video",
  "status": "completed",
  "progress": 100,
  "seconds": "10.0",
  "size": "1280x768",
  "remixed_from_video_id": "https://storage.googleapis.com/agnes-aigc/.../video_xxx.mp4",
  "error": null
}
```

The video download URL is in `remixed_from_video_id`.

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

### Error Codes

| Code | Description |
|------|-------------|
| 400 | Invalid request parameters |
| 401 | Unauthorized — check API key |
| 404 | Task or video not found |
| 500 | Server error |
| 503 | Service busy, retry later |
