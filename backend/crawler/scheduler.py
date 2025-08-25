import asyncio
import os
import json
from pathlib import Path
import urllib.parse

from data_crawler import crawl_shop_details, crawl_tournament_details, crawl_init_links
from data_process_to_json import extract_json

from db_models import Tournament, Shop
from db_utils_orm import MySQLHelper


MYSQL_CONF_MAP = {
    'TEST':{
        "host": "0.0.0.0",
        "port": 3306,
        "user": "root",
        "passwd": "root",
        "db": "test",
    },
    'ONLINE': {
        "host": "0.0.0.0",
        "port": 3306,
        "user": "root",
        "passwd": "root",
        "db": "test",
    }
}

# 从环境变量获取环境信息
env = os.getenv('ENV', 'TEST').upper()
print(f"当前环境: {env}")

db_helper = MySQLHelper(
    user=MYSQL_CONF_MAP.get(env)["user"],
    password=MYSQL_CONF_MAP.get(env)["passwd"],
    host=MYSQL_CONF_MAP.get(env)["host"],
    port=MYSQL_CONF_MAP.get(env)["port"],
    database=MYSQL_CONF_MAP.get(env)["db"]
)


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
        save_to_file(json_data, f'py-script/data/shop/{file_name}')


def process_tournament_details_to_json(tournament_details):
    for detail in tournament_details:
        md_data = detail.markdown
        file_name = detail.url.split('/')[-1]
        # 保存原始的md文件
        save_to_file(md_data, f'py-script/data/tournament/md/{file_name}')
        # 使用ai接口，提取json格式内容
        json_data = extract_json(md_data)
        json_data = json.loads(json_data)
        if not json_data:
            continue
        json_data['event_id'] = int(file_name)
        json_data['event_link'] = detail.url
        # 保存json格式文件
        save_to_file(json_data, f'py-script/data/tournament/json/{file_name}')


# 保存shop数据到数据库
def save_shop_to_db():
    shop_ids = scan_file_ids("py-script/data/shop/")
    print('exits_shop_ids: ' + str(len(shop_ids)))
    for id in shop_ids:
        existing = db_helper.query_filter(Shop, shop_id=id)
        if existing:
            print(f"ℹ️ 商店数据已存在: {id}")
            continue

        with open(f'py-script/data/shop/{id}', 'r', encoding='utf-8') as f:
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
            db_helper.add(shop)
        print(f"✅ 新增商店数据: {id}")


def save_tournament_to_db():
    tourney_ids = scan_file_ids("py-script/data/tournament/json/")
    print('exits_tourney_ids: ' + str(len(tourney_ids)))
    for id in tourney_ids:
        existing = db_helper.query_filter(Tournament, event_id=id)
        if existing:
            print(f"ℹ️ 赛事数据已存在: {id}")
            continue

        with open(f'py-script/data/tournament/json/{id}', 'r', encoding='utf-8') as f:
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
            db_helper.add(tournament)
        print(f"✅ 新增赛事数据: {id}")


# 扫描文件夹下的文件名列表
def scan_file_ids(folder_path):
    return [f.name for f in Path(folder_path).iterdir() if f.is_file()]


async def main():
    init_all_shop = False
    init_all_tournament = False

    # 已保存的shop信息
    saved_shop_ids = scan_file_ids("py-script/data/shop/")
    print('saved_shop_ids: ' + str(len(saved_shop_ids)))
    # 已保存的tournament信息
    saved_tourney_ids = scan_file_ids("py-script/data/tournament/json/")
    print('saved_tourney_ids: ' + str(len(saved_tourney_ids)))

    # 爬取tourney和shop的链接
    tourney_links, shop_links = await crawl_init_links()
    print('tourney_links: ' + str(len(tourney_links)))
    print('shop_links: ' + str(len(shop_links)))

    #判断哪些是新的链接，仅处理新链接 
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

    # 爬取新的shop和tournament详情
    # shop_details = await crawl_shop_details(new_shop_links)
    # process_shop_details_to_json(shop_details)
    tourney_details = await crawl_tournament_details(new_tourney_links)
    process_tournament_details_to_json(tourney_details)

    save_shop_to_db()
    save_tournament_to_db()


if __name__ == "__main__":
    asyncio.run(main())

