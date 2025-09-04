#!/bin/bash

# 进入脚本所在的目录
cd /home/ubuntu/poker-finder
. venv/bin/activate

# 获取天数参数，1=明天，2=后天，3=大后天，默认为1
if [ -n "$1" ]; then
    OFFSET="$1"
else
    OFFSET=1
fi

# 计算目标日期
DATE=$(date -d "$OFFSET day" '+%Y-%m-%d')

nohup python backend/crawler/scheduler.py --date "$DATE" > crawler.log 2>&1 &
