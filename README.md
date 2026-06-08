# 🎨 Agnes Media Skill

> 🆓 **完全免费** — Agnes AI 图片生成和视频生成 API 当前 **零费用**，每月有免费额度可用！

一个用于调用 [Agnes AI](https://agnes-ai.com) API 生成图片和视频的 Claude Code Skill，支持文生图、图生图、文生视频、图生视频、多图视频和关键帧动画。

## ✨ 功能特性

### 🖼️ 图片生成 (agnes-image-2.1-flash)
- **文生图** — 从文字描述生成高质量图片
- **图生图** — 基于已有图片进行风格转换、场景变换
- 支持自定义尺寸（1024x768、768x1024、1024x1024 等）
- 支持 URL 或 Base64 输出

### 🎬 视频生成 (agnes-video-v2.0)
- **文生视频** — 从文字描述生成电影级视频
- **图生视频** — 将静态图片动画化
- **多图视频** — 使用多张参考图引导视频生成
- **关键帧动画** — 在多个关键帧之间生成平滑过渡动画
- 支持时长控制（3s ~ 18s）、分辨率、帧率自定义
- 异步任务处理，自动轮询进度

## 💰 定价

| 服务 | 原价 | 当前价格 |
|------|------|---------|
| 图片生成 | ~~$0.003/张~~ | **🆓 $0** |
| 视频生成 | ~~$0.005/秒~~ | **🆓 $0** |

> 在 https://agnes-ai.com 注册即可获取免费 API Key。

## 🚀 快速开始

### 1. 获取 API Key

前往 https://agnes-ai.com 注册账号并获取 API Key。

### 2. 设置环境变量

```bash
export AGNES_API_KEY="your-api-key-here"
```

### 3. 生成图片

```bash
# 文生图
python agnes-media/scripts/agnes_media.py image \
  --prompt "一座漂浮在迷雾峡谷上方的发光城市，电影级写实风格" \
  --size 1024x768 \
  --output output.png

# 图生图
python agnes-media/scripts/agnes_media.py image \
  --prompt "将场景转换为赛博朋克夜景，保留原始构图" \
  --size 1024x768 \
  --image-url "https://example.com/input.png" \
  --output transformed.png
```

### 4. 生成视频

```bash
# 文生视频（~5秒）
python agnes-media/scripts/agnes_media.py video \
  --prompt "一只猫在日落时的海滩上漫步，柔和的海浪，温暖的金色光线" \
  --width 1152 --height 768 \
  --num-frames 121 --frame-rate 24 \
  --output video.mp4

# 图生视频
python agnes-media/scripts/agnes_media.py video \
  --prompt "角色缓缓转身面向镜头，自然表情，电影级运镜" \
  --image-url "https://example.com/character.png" \
  --output animated.mp4

# 关键帧动画
python agnes-media/scripts/agnes_media.py video \
  --prompt "两个场景之间的平滑过渡" \
  --mode keyframes \
  --extra-images "https://example.com/kf1.png" "https://example.com/kf2.png" \
  --output transition.mp4
```

## 📐 视频时长参考

| 目标时长 | num_frames | frame_rate |
|---------|-----------|------------|
| ~3 秒 | 81 | 24 |
| ~5 秒 | 121 | 24 |
| ~10 秒 | 241 | 24 |
| ~18 秒 | 441 | 24 |

> `num_frames` 必须遵循 `8n + 1` 规则，最大值 441。

## 📁 项目结构

```
agnes-media/
├── SKILL.md                        # Skill 主文件（触发描述 + 使用指南）
├── scripts/
│   └── agnes_media.py              # 核心 Python 脚本
└── references/
    └── api_reference.md            # 完整 API 参考文档
```

## 🔧 作为 Claude Code Skill 使用

将 `agnes-media` 文件夹放入你的 skill 目录，Claude Code 即可自动识别并在用户请求生成图片/视频时调用。

安装打包好的 skill：
```
agnes-media.skill
```

## 📝 Prompt 技巧

**图片提示词结构**：
```
[主体] + [场景/环境] + [风格] + [光线] + [构图] + [质量要求]
```

**视频提示词结构**：
```
[主体] + [动作] + [场景] + [运镜方式] + [光线] + [风格]
```

**图生图/视频**：务必同时描述变化部分和保留部分（例如："将场景转换为赛博朋克风格，保留原始构图"）。

## 📄 许可证

MIT License

## 🔗 链接

- [Agnes AI 官网](https://agnes-ai.com)
- [Agnes Image 2.1 Flash 文档](https://agnes-ai.com/doc/agnes-image-21-flash)
- [Agnes Video V2.0 文档](https://agnes-ai.com/doc/agnes-video-v20)
