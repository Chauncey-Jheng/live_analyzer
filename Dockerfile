# 使用官方 Python 镜像作为基础镜像
FROM python:3.11-slim

# 安装tmux 和 ffmpeg
RUN apt-get update && apt-get install -y tmux && apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

COPY . /app

# 安装依赖包
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install -r requirements.txt
