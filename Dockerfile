FROM python:3.11-alpine

COPY --from=ghcr.io/astral-sh/uv:python3.11-alpine /usr/local/bin/uv /usr/local/bin/uvx /bin/

WORKDIR /app

COPY . .

RUN apk update && apk add ffmpeg curl && rm -rf /var/cache/apk/* && uv sync && uv cache clean

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
