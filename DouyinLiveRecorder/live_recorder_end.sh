#!/bin/bash

# 关闭 main.py 运行所在的tmux会话
tmux kill-session -t live_recorder_main

# 关闭名为 monitor.py 运行所在的tmux会话
tmux kill-session -t live_recorder_monitor

echo "tmux会话已关闭。"
