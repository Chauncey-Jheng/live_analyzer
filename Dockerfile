# 使用官方 Python 镜像作为基础镜像
FROM nvcr.io/nvidia/pytorch:23.08-py3

# 安装tmux 和 ffmpeg
RUN apt-get update && apt-get install -y tmux && apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

COPY . /app

# 安装依赖包
RUN pip install -r requirements.txt

# 修复opencv-python依赖库
RUN python -c "from opencv_fixer import AutoFix; AutoFix()"
