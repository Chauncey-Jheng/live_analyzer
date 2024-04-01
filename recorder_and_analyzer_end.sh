#!/bin/bash

# 关闭 main.py 运行所在的tmux会话
tmux kill-session -t live_recorder_main

# 关闭 monitor.py 运行所在的tmux会话
tmux kill-session -t live_recorder_monitor

# 关闭 live_analyzer.py 运行所在的tmux会话
tmux kill-session -t live_analyzer

echo "tmux会话已关闭。"
