#!/bin/bash
# 启动虚拟环境
source ../venv/bin/activate

# 设置 Flask 运行入口和关闭调试
export FLASK_APP=server.py
export FLASK_ENV=production

# 运行 Flask 应用在后台（使用 tmux）
SESSION="flask-server"

# 如果 tmux session 不存在就创建并启动 Flask
if ! tmux has-session -t $SESSION 2>/dev/null; then
    echo "Starting Flask in tmux session '$SESSION'..."
    tmux new-session -d -s $SESSION "flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1"
else
    echo "Flask already running in tmux session '$SESSION'"
fi