#!/bin/bash

llamafile="Meta-Llama-3-8B-Instruct.Q5_K_M.llamafile"
# llamafile="Mistral-7b-instruct-v0.2.Q4_0.llamafile"
#llamafile="rocket-3b.Q5_K_M.llamafile"
# llamafile="llava-v1.5-7b-q4.llamafile"
#llamafile="phi-2.Q5_K_M.llamafile"
if ! tmux has-session -t llamafile_server 2>/dev/null; then
	tmux new-session -d -s llamafile_server "./models/llm/${llamafile} -ngl 9999 --host 0.0.0.0 --port 8080 --ctx-size 2048"
	echo "tmux 会话 llamafile_server 创建完成"
else
	echo "tmux 会话 llamafile_server 已经存在，跳过创建"
fi
