import asyncio
import os
import json
from pathlib import Path
import urllib.parse
import logging

from data_crawler import crawl_shop_details, crawl_tournament_details, crawl_init_links
from data_process_to_json import extract_json

from models.tournament_model import Tournament
from models.shop_model import Shop

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
DATA_PATH = "./data"



def save_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        if isinstance(data, (dict, list)):
            # 把data转化成json字符串
            data = json.dumps(data, ensure_ascii=False, indent=2)
        if data:
            f.write(data)


def process_shop_details_to_json(shop_details):
    for detail in shop_details:
        json_data = json.loads(detail.extracted_content)
        if not json_data:
            continue
        json_data = json_data[0]  # 取第一个元素
        file_name = detail.url.split('/')[-1]
        json_data['shop_id'] = int(file_name)
        json_data['shop_link'] = detail.url
        json_data['map_link'] = urllib.parse.unquote(json_data.get('map_link', ''))
        # 保存原始的json格式文件
        save_to_file(json_data, DATA_PATH + f'/shop/{file_name}')


def process_tournament_details_to_json(tournament_details):
    for detail in tournament_details:
        md_data = detail.markdown
        file_name = detail.url.split('/')[-1]
        # 保存原始的md文件
        save_to_file(md_data, DATA_PATH + f'/tournament/md/{file_name}')
        # 使用ai接口，提取json格式内容
        json_data = extract_json(md_data)
        logging.info(f"extract_json, file_name: {file_name}")
        json_data = json.loads(json_data)
        if not json_data:
            continue
        json_data['event_id'] = int(file_name)
        json_data['event_link'] = detail.url
        save_to_file(json_data, DATA_PATH + f'/tournament/json/{file_name}')


def save_shop_to_db():
    shop_ids = scan_file_ids(DATA_PATH + "/shop/")
    logging.info('exits_shop_ids: ' + str(len(shop_ids)))
    for id in shop_ids:
        existing = Shop.query.filter_by(shop_id=id).first()
        if existing:
            logging.info(f"ℹ️ 商店数据已存在: {id}")
            continue
        with open(DATA_PATH + f'/shop/{id}', 'r', encoding='utf-8') as f:
            json_data = f.read()
            if not json_data:
                continue
            json_obj = json.loads(json_data)
            shop = Shop(
                shop_id = json_obj.get('shop_id', 0),
                shop_link = json_obj.get('shop_link', ''),
                shop_name = json_obj.get('shop_name', ''),
                address = json_obj.get('address', ''),
                map_link =  json_obj.get('map_link', ''),
                phone = json_obj.get('phone', ''),
                homepage = json_obj.get('homepage', ''),
                business_hours = json_obj.get('business_hours', '')
            )
            Shop.add(shop)
        logging.info(f"✅ 新增商店数据: {id}")

def save_tournament_to_db():
    tourney_ids = scan_file_ids(DATA_PATH + "/tournament/json/")
    logging.info('exits_tourney_ids: ' + str(len(tourney_ids)))
    for id in tourney_ids:
        existing = Tournament.query.filter_by(event_id=id).first()
        if existing:
            logging.info(f"ℹ️ 赛事数据已存在: {id}")
            continue
        with open(DATA_PATH + f'/tournament/json/{id}', 'r', encoding='utf-8') as f:
            json_data = f.read()
            if not json_data:
                continue
            json_obj = json.loads(json_data)
            tournament = Tournament(
                event_id = json_obj.get('event_id', 0),
                event_link = json_obj.get('event_link', ''),
                event_name = json_obj.get('event_name', ''),
                status = json_obj.get('status', ''),
                shop_id = json_obj.get('shop_id', 0),
                shop_name = json_obj.get('shop_name', 0),
                official_page = json_obj.get('official_page', ''),
                start_time = json_obj.get('start_time', ''),
                game_rule = json_obj.get('game_rule', ''),
                entry_fee = json_obj.get('entry_fee', 0),
                re_entry = json_obj.get('re_entry', ''),
                prizes = json.dumps(json_obj.get('prizes', '')),
                prizes_original = json_obj.get('prizes_original', ''),
                address = json_obj.get('address', ''),
                prefecture = json_obj.get('prefecture', ''),
                city_ward = json_obj.get('city_ward', ''),
                tel = json_obj.get('tel', ''),
                total_winners = json_obj.get('prizes_analyze', {}).get('total_winners', 0),
                total_value_jpy = json_obj.get('prizes_analyze', {}).get('total_value_jpy', 0),
                reward_categories = ','.join(json_obj.get('prizes_analyze', {}).get('reward_categories', [])),
                rank_list = json.dumps(json_obj.get('prizes_analyze', {}).get('rank_list', []), ensure_ascii=False)
            )
            Tournament.add(tournament)
        logging.info(f"✅ 新增赛事数据: {id}")


def scan_file_ids(folder_path):
    return [f.name for f in Path(folder_path).iterdir() if f.is_file()]


async def main():
    init_all_shop = False
    init_all_tournament = False
    saved_shop_ids = scan_file_ids(DATA_PATH + "/shop/")
    logging.info('saved_shop_ids: ' + str(len(saved_shop_ids)))
    saved_tourney_ids = scan_file_ids(DATA_PATH + "/tournament/json/")
    logging.info('saved_tourney_ids: ' + str(len(saved_tourney_ids)))
    tourney_links, shop_links = await crawl_init_links()
    logging.info('tourney_links: ' + str(len(tourney_links)))
    logging.info('shop_links: ' + str(len(shop_links)))

    new_shop_links = []
    if init_all_shop:
        new_shop_links = shop_links
    else:
        for link in shop_links:
            if link.split("/")[-1] not in saved_shop_ids:
                new_shop_links.append(link)
    new_tourney_links = []
    if init_all_tournament:
        new_tourney_links = tourney_links
    else:
        for link in tourney_links:
            if link.split("/")[-1] not in saved_tourney_ids:
                new_tourney_links.append(link)


    shop_details = await crawl_shop_details(new_shop_links[:10])
    process_shop_details_to_json(shop_details)
    tourney_details = await crawl_tournament_details(new_tourney_links[:10])
    process_tournament_details_to_json(tourney_details)

    save_shop_to_db()
    save_tournament_to_db()
if __name__ == "__main__":
    asyncio.run(main())
