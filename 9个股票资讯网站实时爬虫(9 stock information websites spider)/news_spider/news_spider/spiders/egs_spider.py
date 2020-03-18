# -*- coding: utf-8 -*-
'''
 用于爬取e公司的爬虫
 author:MingKnight
 date:2019-5-16
 versoin: 1.0.0
'''
import scrapy
from news_spider.items import NewsItem, ErrorItem
import time
import json
from news_spider import settings
import random


class EgsSpiderSpider(scrapy.Spider):
    name = 'egs_spider'
    allowed_domains = ['egs.stcn.com']
    custom_settings = {
        # 'LOG_FILE': name + '.log',
        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS':32,
        'CONCURRENT_ITEMS':32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'DOWNLOAD_TIMEOUT':0.6,
    }
    def start_requests(self):
        base_url = "http://egs.stcn.com/news/flash-list?important=1&normal=1&page=1&pageTime=0&per-page=10"
        while True:
            time.sleep(settings.global_sleep_time)
            yield scrapy.Request(url=base_url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        if response.status == 200:
            try:
                data = json.loads(response.body.decode())
            except Exception as e:
                print(e)
                item = ErrorItem()
                item['code'] = response.status
                # 出错的页面
                item['url'] = 901
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的url
                item['site'] = "e公司"
                # 出错的描述
                item['desc'] = '响应的json数据错误'
                # 代码报出的错误
                item['exception'] = str(e)
                return item
            else:
                try:
                    for item in data['data']:
                        i = NewsItem()
                        i['source'] = "egs"
                        # print(item)
                        i['pubDate'] = item.get('pageTime', "")
                        i['title'] = item.get('title', "")
                        i['content'] = item.get('content', "")
                        i['isRed'] = item.get('isRed', 0)
                        yield i
                except Exception as e:
                    item = ErrorItem()
                    item['code'] = response.status
                    # 出错的页面
                    item['url'] = 902
                    # 出错的时间
                    # item['timestamp'] = time.time()
                    # 出错的url
                    item['site'] = "e公司"
                    # 出错的描述
                    item['desc'] = '解析json数据错误'
                    # 代码报出的错误
                    item['exception'] = str(e)
                    yield item
        else:
            item = ErrorItem()
            item['code'] = response.status
            # 出错的页面
            item['url'] = response.url
            # 出错的时间
            # item['timestamp'] = time.time()
            # 出错的url
            item['site'] = "e公司"
            # 出错的描述
            item['desc'] = '响应错误'
            # 代码报出的错误
            item['exception'] = ''
            yield item
