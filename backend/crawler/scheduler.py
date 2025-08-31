import asyncio
import os
import json
from pathlib import Path
import logging
import re
import time

from backend.crawler.data_crawler import crawl_tournament_details, crawl_init_links
from backend.crawler.ai_agent import query_ai
from backend.models.tournament_model import Tournament
from backend.server import create_app
from backend.db import db

app = create_app()

def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

# 初始化日志
init_logging()

# 从环境变量获取环境信息
env = os.getenv('ENV', 'TEST').upper()
logging.info(f"当前环境: {env}")
DATA_PATH = "backend/crawler/data"
base_url = "https://pokerguild.jp"


def extract_date(start_time_str):
    # 匹配形如 2025/08/29 的日期部分
    match = re.search(r'(\d{4})/(\d{2})/(\d{2})', start_time_str)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month}-{day}"
    return None

def extract_entry_fee(entry_fee_str):
    # 去掉非数字字符，只保留数字
    fee = re.sub(r'[^\d]', '', entry_fee_str)
    return int(fee) if fee else None

def save_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        if isinstance(data, (dict, list)):
            data = json.dumps(data, ensure_ascii=False, indent=2)
        if data:
            f.write(data)


def process_tournament_details_to_json(tournament_details):
    for detail in tournament_details:
        file_name = detail.url.split('/')[-1]
        md_data = detail.markdown
        json_data = json.loads(detail.extracted_content)[0]
        json_data['shop_id'] = json_data['shop_link'].split('/')[-1]
        json_data['shop_link'] = base_url + json_data['shop_link']
        json_data['event_id'] = int(file_name)
        json_data['event_link'] = detail.url
        #"start_time": "2025/08/29 13:00〜",
        json_data['start_date'] = extract_date(json_data['start_time'])
        # "entry_fee": "2,500円",
        json_data['entry_fee'] = extract_entry_fee(json_data['entry_fee'])
        saved_data = {
            'md_data': md_data,
            'json_data': json_data
        }
        # 结合ai，提取json格式内容
        ai_data = query_ai(saved_data)
        if not ai_data:
            continue
        saved_data['ai_data'] = ai_data

        saved_data = json.dumps(saved_data, ensure_ascii=False, indent=2)
        save_to_file(saved_data, DATA_PATH + f'/tournament/json/{file_name}')
        time.sleep(0.2)


def save_tournament_to_db():
    tourney_ids = scan_file_ids(DATA_PATH + "/tournament/json/")
    logging.info('exits_tourney_ids: ' + str(len(tourney_ids)))
    for id in tourney_ids:
        existing = Tournament.query.filter_by(event_id=id).first()
        if existing:
            logging.info(f"ℹ️ 赛事数据已存在: {id}")
            continue
        with open(DATA_PATH + f'/tournament/json/{id}', 'r', encoding='utf-8') as f:
            file_data = f.read()
            if not file_data:
                continue
            file_data = json.loads(file_data)
            json_data = file_data["json_data"]
            ai_data = file_data["ai_data"]
            md_data = file_data["md_data"]
            tournament = Tournament(
                event_id = json_data["event_id"],
                event_name = json_data["event_name"],
                event_link = json_data["event_link"],
                entry_fee = json_data["entry_fee"],
                shop_id = json_data["shop_id"],
                shop_name = json_data["shop_name"],
                shop_link = json_data["shop_link"],
                official_page = json_data["official_page"],
                
                start_date = ai_data["start_date"],
                start_time = ai_data["start_time"],
                late_time = ai_data["late_time"],
                reward_categories = json.dumps(ai_data["reward_categories"], ensure_ascii=False, indent=2),
                reward_summary = ai_data["reward_summary"],
                prefecture = ai_data["prefecture"],
                city_ward = ai_data["city_ward"],
                
                prizes_original = md_data,
            )
            db.session.add(tournament)
            db.session.commit()
        logging.info(f"✅ 新增赛事数据: {id}")


def scan_file_ids(folder_path):
    return [f.name for f in Path(folder_path).iterdir() if f.is_file()]


async def main():
    init_all_tournament = False
    saved_tourney_ids = scan_file_ids(DATA_PATH + "/tournament/json/")
    logging.info('saved_tourney_ids: ' + str(len(saved_tourney_ids)))
    tourney_links, _ = await crawl_init_links()
    logging.info('tourney_links: ' + str(len(tourney_links)))

    new_tourney_links = []
    if init_all_tournament:
        new_tourney_links = tourney_links
    else:
        for link in tourney_links:
            if link.split("/")[-1] not in saved_tourney_ids:
                new_tourney_links.append(link)
    tourney_details = await crawl_tournament_details(new_tourney_links)
    process_tournament_details_to_json(tourney_details)
    with app.app_context():
        save_tournament_to_db()

if __name__ == "__main__":
    asyncio.run(main())
