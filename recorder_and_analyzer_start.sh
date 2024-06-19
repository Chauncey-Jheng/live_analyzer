#!/bin/bash

cd ./DouyinLiveRecorder

# 检查是否存在名为live_recorder_main的tmux会话
if ! tmux has-session -t live_recorder_main 2>/dev/null; then
    # 如果不存在，创建tmux会话并运行Python脚本 main.py
    tmux new-session -d -s live_recorder_main 'python main.py'
    echo "tmux会话 live_recorder_main 创建完成"
else
    echo "tmux会话 live_recorder_main已存在，跳过创建"
fi

# 检查是否存在名为live_recorder_monitor的tmux会话
if ! tmux has-session -t live_recorder_monitor 2>/dev/null; then
    # 如果不存在，创建tmux会话并运行Python脚本 monitor.py
    tmux new-session -d -s live_recorder_monitor 'python monitor.py'
    echo "tmux会话 live_recorder_monitor 创建完成"
else
    echo "tmux会话 live_recorder_monitor已存在，跳过创建"
fi

cd ..

llamafile="Meta-Llama-3-8B-Instruct.Q5_K_M.llamafile"
# llamafile="Mistral-7b-instruct-v0.2.Q4_0.llamafile"
#llamafile="rocket-3b.Q5_K_M.llamafile"
# llamafile="llava-v1.5-7b-q4.llamafile"
#llamafile="phi-2.Q5_K_M.llamafile"
if ! tmux has-session -t llamafile_server 2>/dev/null; then
	tmux new-session -d -s llamafile_server "./models/llm/${llamafile} -ngl 9999 --host 0.0.0.0 --port 8080"
	echo "tmux 会话 llamafile_server 创建完成"
else
	echo "tmux 会话 llamafile_server 已经存在，跳过创建"
fi

# 检查是否存在名为live_analyzer的tmux会话
if ! tmux has-session -t live_analyzer 2>/dev/null; then
    # 如果不存在，创建tmux会话并运行Python脚本 analyzer.py
    tmux new-session -d -s live_analyzer 'python live_analyzer.py'
    echo "tmux会话 live_analyzer 创建完成"
else
    echo "tmux会话 live_analyzer已存在，跳过创建"
fi

echo "Python脚本已在后台运行，并在各自的tmux会话中。"