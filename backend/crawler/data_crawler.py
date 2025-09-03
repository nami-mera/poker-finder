import asyncio
import os
from urllib.parse import urlencode
import json
import time
from datetime import datetime, timedelta


from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai import JsonCssExtractionStrategy
from crawl4ai.async_webcrawler import AsyncWebCrawler, CacheMode
from crawl4ai.async_configs import CrawlerRunConfig
from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher, RateLimiter
from crawl4ai.extraction_strategy import JsonXPathExtractionStrategy

BASE_URL = "https://pokerguild.jp/"
default_start_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

params = {
    # "tourneyname": "",
    # "venue": "",
    "start_date_from": default_start_date,
    "start_date_to": default_start_date,
    # "limit": "",
    # "game": "",
    # "exclude": "0"
}
search_url = BASE_URL + "tourneys?" + urlencode(params)

VERBOSE = False

schema_of_shop_xpath = {
    "name": "shop_info",
    "baseSelector": "//table[@class='table table-striped']",
    "fields": [
        {"name": "shop_name", "selector": ".//th[contains(text(),'店舗名')]/following-sibling::td", "type": "text"},
        {
            "name": "address",
            "selector": ".//th[contains(text(),'住所')]/following-sibling::td/a",
            "type": "text"
        },
        {
            "name": "map_link",
            "selector": ".//th[contains(text(),'住所')]/following-sibling::td/a",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "phone",
            "selector": ".//th[contains(text(),'電話番号')]/following-sibling::td/a",
            "type": "text"
        },
        {
            "name": "homepage",
            "selector": ".//th[contains(text(),'ホームページ')]/following-sibling::td/a",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "business_hours",
            "selector": ".//th[contains(text(),'営業時間')]/following-sibling::td",
            "type": "text"
        }
    ]
}
schema_of_tournament_xpath = {
    "name": "tournament_info",
    # 只选第一个panel（主赛事信息）
    "baseSelector": "//div[contains(@class, 'col-md-8')]/main/div[contains(@class, 'panel') and contains(@class, 'panel-pg-default')][1]",
    "fields": [
        {
            "name": "event_name",
            "selector": ".//div[contains(@class, 'panel-heading')]",
            "type": "text"
        },
        {
            "name": "shop_name",
            "selector": ".//th[contains(text(),'店舗名')]/following-sibling::td[1]/a",
            "type": "text"
        },
        {
            "name": "shop_link",
            "selector": ".//th[contains(text(),'店舗名')]/following-sibling::td[1]/a",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "official_page",
            "selector": ".//th[contains(text(),'公式ページ')]/following-sibling::td[1]/a",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "start_time",
            "selector": ".//th[contains(text(),'開始日時')]/following-sibling::td[1]",
            "type": "text"
        },
        {
            "name": "entry_fee",
            "selector": ".//th[contains(text(),'参加費')]/following-sibling::td[1]",
            "type": "text"
        }
    ]
}


async def crawl_links(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
            )
        )
        links = result.links["internal"] # pyright: ignore[reportAttributeAccessIssue]
        tourney_links = [link['href'] for link in links if '/tourneys/' in link['href']]
        shop_links = [link['href'] for link in links if '/venues/' in link['href']]
        return tourney_links, shop_links


async def crawl_link_detail(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                verbose=VERBOSE,
                css_selector="div.col-md-8"
            )
        )
        return result


async def crawl_parallel_dispatcher(urls, config):
    # Dispatcher with rate limiter enabled (default behavior)
    dispatcher = MemoryAdaptiveDispatcher(
        rate_limiter=RateLimiter(
            base_delay=(1.0, 3.0),
            max_delay=20.0,
            max_retries=3,
            rate_limit_codes=[429, 503]
        ),
        max_session_permit=3,
    )
    start_time = time.perf_counter()
    async with AsyncWebCrawler() as crawler:
        result_container = await crawler.arun_many(urls=urls, config=config, dispatcher=dispatcher)
        results = []
        if isinstance(result_container, list):
            results = result_container
        else:
            async for res in result_container: # pyright: ignore[reportGeneralTypeIssues]
                results.append(res)
    total_time = time.perf_counter() - start_time
    print(f"Total time: {total_time} seconds")
    return results



async def crawl_by_css():
    schema = {
        "name": "poker_tournaments",
        "baseSelector": "div.table-pg-responsive > table > tbody > tr",
        "fields": [
            {"name": "start_date", "selector": "td.col-xs-2", "type": "text"},
            {"name": "tournament_name", "selector": "td.col-xs-7 > a", "type": "text"},
            {"name": "tournament_type", "selector": "td.col-xs-7", "type": "text"},
            {"name": "tournament_link", "selector": "td.col-xs-7 > a", "type": "attribute", "attribute": "href"},
            {"name": "shop_name", "selector": "td.col-xs-3 > a", "type": "text"},
            {"name": "shop_link", "selector": "td.col-xs-3 > a", "type": "attribute", "attribute": "href"},
            {"name": "shop_addr", "selector": "td.col-xs-3", "type": "text"},
        ]
    }
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=search_url,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(schema),
            )
        )
        data = json.loads(result.extracted_content) # type: ignore
        print(data)
    

async def crawl_by_xpath():
    schema = {
        "name": "poker_tournaments",
        "baseSelector": "//table[@class='table table-striped']/tbody/tr",
        "fields": [
            {"name": "start_date", "selector": ".//td[@class='col-xs-2']", "type": "text"},
            {"name": "tournament_name", "selector": ".//td[@class='col-xs-7']/a", "type": "text"},
            {"name": "tournament_link", "selector": ".//td[@class='col-xs-7']/a", "type": "attribute", "attribute": "href"},
            {"name": "shop_name", "selector": ".//td[@class='col-xs-3']/a", "type": "text"},
            {"name": "shop_link", "selector": ".//td[@class='col-xs-3']/a", "type": "attribute", "attribute": "href"}
        ]
    }

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=search_url,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonXPathExtractionStrategy(schema, verbose=True)
            )
        )
        data = json.loads(result.extracted_content) # pyright: ignore[reportAttributeAccessIssue]
        print(data)


async def crawl_by_table():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=search_url,
            config=CrawlerRunConfig(
                table_score_threshold=7  # Minimum score for table detection
            )
        )

        if result.success and result.tables: # type: ignore
            print(f"Found {len(result.tables)} tables") # pyright: ignore[reportAttributeAccessIssue]

            for i, table in enumerate(result.tables): # pyright: ignore[reportAttributeAccessIssue]
                print(f"\nTable {i+1}:")
                print(f"Caption: {table.get('caption', 'No caption')}")
                print(f"Headers: {table['headers']}")
                print(f"Rows: {len(table['rows'])}")

                # Print first few rows as example
                for j, row in enumerate(table['rows'][:3]):
                    print(f"  Row {j+1}: {row}")


def save_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)



# 爬取shop的详情, 返回json格式
async def crawl_shop_details(shop_links):
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        css_selector="div.col-md-8",
        extraction_strategy=JsonXPathExtractionStrategy(schema_of_shop_xpath)
    )
    shop_details = await crawl_parallel_dispatcher(shop_links, config)
    print('shop_details: ' + str(len(shop_details)))    
    return shop_details


# 爬取tournament的详情, 返回md格式
async def crawl_tournament_details(tournament_links):
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        css_selector="div.col-md-8",
        extraction_strategy=JsonXPathExtractionStrategy(schema_of_tournament_xpath)
    )
    tourney_details = await crawl_parallel_dispatcher(tournament_links, config)
    print('tourney_details: ' + str(len(tourney_details)))
    return tourney_details


# 爬取tourney和shop的链接
async def crawl_init_links(date):
    params = {
        # "tourneyname": "",
        # "venue": "",
        "start_date_from": date if date else default_start_date,
        "start_date_to": date if date else default_start_date,
        # "limit": "",
        # "game": "",
        # "exclude": "0"
    }
    search_url = BASE_URL + "tourneys?" + urlencode(params)
    return await crawl_links(search_url)


if __name__ == "__main__":
    # list_result = asyncio.run(crawl_by_css())
    # asyncio.run(crawl_by_xpath())
    # asyncio.run(crawl_by_table())

    # 爬取tourney和shop的链接
    tourney_links, shop_links = asyncio.run(crawl_links(search_url))
    print('tourney_links: ' + str(len(tourney_links)))

    # 爬取tourney的详情,markdown格式
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        css_selector="div.col-md-8",
        # target_elements=["article.main-content", "aside.sidebar"],
        extraction_strategy=JsonXPathExtractionStrategy(schema_of_tournament_xpath)
    )
    tourney_details = asyncio.run(crawl_parallel_dispatcher(tourney_links[:1], config))
    print('tourney_details: ' + str(len(tourney_details)))
    for detail in tourney_details:
        md_data = detail.markdown
        json_data = json.loads(detail.extracted_content)
        file_name = detail.url.split('/')[-1]
        data = {
            'md_data': md_data,
            'json_data': json_data
        }
        data = json.dumps(data, ensure_ascii=False, indent=2)
        save_to_file(data, f'backend/crawler/data/tournament/json_test/{file_name}.test.json')


    # result = asyncio.run(crawl_link_detail('https://pokerguild.jp/tourneys/314098'))
    # print(result.markdown)


