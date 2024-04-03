#!/bin/bash

cd ./DouyinLiveRecorder

# 检查是否存在名为live_recorder_main的tmux会话
if ! tmux has-session -t live_recorder_main 2>/dev/null; then
    # 如果不存在，创建tmux会话并运行Python脚本 main.py
    tmux new-session -d -s live_recorder_main 'conda activate live_analyzer && python main.py'
    echo "tmux会话 live_recorder_main 创建完成"
else
    echo "tmux会话 live_recorder_main已存在，跳过创建"
fi

# 检查是否存在名为live_recorder_monitor的tmux会话
if ! tmux has-session -t live_recorder_monitor 2>/dev/null; then
    # 如果不存在，创建tmux会话并运行Python脚本 monitor.py
    tmux new-session -d -s live_recorder_monitor 'conda activate live_analyzer && python monitor.py'
    echo "tmux会话 live_recorder_monitor 创建完成"
else
    echo "tmux会话 live_recorder_monitor已存在，跳过创建"
fi

cd ..

# 检查是否存在名为live_analyzer的tmux会话
if ! tmux has-session -t live_analyzer 2>/dev/null; then
    # 如果不存在，创建tmux会话并运行Python脚本 analyzer.py
    tmux new-session -d -s live_analyzer 'conda activate live_analyzer && python live_analyzer.py'
    echo "tmux会话 live_analyzer 创建完成"
else
    echo "tmux会话 live_analyzer已存在，跳过创建"
fi

echo "Python脚本已在后台运行，并在各自的tmux会话中。"