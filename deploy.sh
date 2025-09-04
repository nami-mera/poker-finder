#!/bin/bash

# 进入脚本所在的目录
cd /home/ubuntu/poker-finder
. venv/bin/activate

# 设置 Flask 运行入口和关闭调试
export FLASK_APP=backend/server.py
export FLASK_ENV=production

# 使用 nohup 启动 Flask 应用在后台
echo "Starting Flask app with nohup..."
nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &

echo "Flask app started with nohup. Logs are in flask.log."