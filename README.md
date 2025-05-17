# Nijigasaki Whisper

一个用于将视频/录音人声转录为为纯文本/SRT字幕脚本的工具。

## 必要条件

- Python >= 3.11
- FFmpeg（需位于 `PATH` 环境变量中）
- OpenAI API【需可访问 gpt-4o-audio-preview 模型（有其他的模型/API也行，如果你知道自己在做什么）】

## 安装依赖

使用 [uv](https://github.com/astral-sh/uv)：

```bash
git clone https://github.com/xkww3n/niigasaki-whisper.git
cd nijigasaki-whisper
uv sync
```

## 配置

编辑 config.json 配置 OpenAI API，如无特殊需求只需填写 `api_key` 字段。

编辑 .streamlit/secrets.toml 使用 Streamlit 内建的用户认证，需要使用支持 OIDC 协议的服务商，如 [Auth0](https://auth0.com/)。记得将 `redirect_uri` 中的 `http://localhost:8501` 部分替换为实际域名和协议（通常为 HTTPS）。

如果你肯定，确定，笃定自己**不需要** Streamlit 的用户认证，可以注释掉 app.py 文件中的 15-20 行。**关闭 Streamlit 的用户认证之后，若不自行配置其他认证机制，将允许所有人消耗你的 API Key 额度。**

## 直接运行

```bash
uv run streamlit run app.py
```

## 使用 Docker

```bash
# 还原所有更改
git checkout .

# 除非你知道自己在做什么，否则不要把你的密钥构建到镜像中！
docker build . -t nijigasaki-whisper

# 构建镜像之后再编辑配置文件
nano config.json
nano .streamlit/secrets.toml

# 如果还编辑了其他文件，记得编辑 docker-compose.yml 映射到容器中
docker compose up -d
```

## 常见问题 / FA♂Q

### 为什么 whisper / gpt-4o-transcribe 用不了

本项目默认使用的是在 Chat Completion API 下工作的 gpt-4o-audio-preview 模型，而 whisper 或 gpt-4o-transcribe 系列模型工作在 Transcriptions API 下。

### 为什么不用 Transcriptions API

首先，whisper 系列模型效果不好，而 gpt-4o-transcribe 系列模型支持的格式太少（我也用不了这个模型因此无法测试）；其次，Transcriptions API 最大只能上传 25MB 的音频文件，太小了不够用。

### 怎么改站点名称

编辑 app.py 。

## 致谢

- [FFmpeg](https://ffmpeg.org/)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
- [openai/openai-python](https://github.com/openai/openai-python)
- [Streamlit](https://streamlit.io/)
- [虹ヶ咲学園スクールアイドル同好会](https://www.lovelive-anime.jp/nijigasaki/about_nijigasaki.php)

## 许可

[MIT](./LICENSE)
