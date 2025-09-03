#!/bin/bash

# 获取date参数，如果未指定则设置为明天日期
if [ -n "$1" ]; then
    DATE="$1"
else
    DATE=$(date -d "next day" '+%Y-%m-%d')
fi

nohup python backend/crawler/scheduler.py --date "$DATE" > crawler.log 2>&1 &
