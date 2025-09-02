#!/bin/bash
# 启动虚拟环境
source ../venv/bin/activate

nohup python backend/crawler/scheduler.py > crawler.log 2>&1 &
