# -*- coding: utf-8 -*-
'''
财联社爬虫

     author:MingKnight
     date:2019-5-17
     version:1.0.0
'''
import scrapy
from news_spider.items import NewsItem, ErrorItem
import time, datetime
import json
from news_spider import settings
import random
import re
import urllib.parse


class ClsSpiderSpider(scrapy.Spider):
    name = 'cls_spider'
    allowed_domains = ['cls.cn']
    # start_urls = ['http://cls.cn/']
    custom_settings = {
        'LOG_FILE': name + '.log',
        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 100,
        'CONCURRENT_ITEMS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'DOWNLOAD_TIMEOUT': 0.6,
    }

    def start_requests(self):
        base_url = 'https://www.cls.cn/'
        while True:
            time.sleep(settings.global_sleep_time)
            yield scrapy.Request(url=base_url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        if response.status == 200:
            try:
                temp = re.findall('__NEXT_DATA__.*module', response.body.decode(), re.S)[0].replace('__NEXT_DATA__ =',
                                                                                                    '').replace(
                    '__NEXT_DATA__', '').replace('module', '').strip()
                data_list = json.loads('[' + temp + ']')
                # print(data_list)
            except Exception as e:
                print(e)
                item = ErrorItem()
                item['code'] = 800
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的网站
                item['site'] = "财联社"
                # 出错的描述
                item['desc'] = '响应的json数据错误'
                # 代码报出的错误
                item['exception'] = str(e)
                yield item
            else:
                try:
                    for data in data_list[0]["props"]['initialState']['telegraph']['dataList']:
                        item = NewsItem()
                        item['source'] = 'cls'

                        item['pubDate'] = data['modified_time']
                        item['title'] = data['title']
                        #
                        if '【' in data['content'] and '】' in data['content']:
                            item['content'] = re.findall('】.*', data['content'])[0].replace("】", '')
                        else:
                            item['content'] = data['content']

                        # TODO
                        item['isRed'] = 0
                        yield item
                except Exception as e:
                    item = ErrorItem()
                    item['code'] = 902
                    # 出错的页面
                    item['url'] = response.url
                    # 出错的时间
                    # item['timestamp'] = time.time()
                    # 出错的网站
                    item['site'] = "财联社"
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
            # 出错的网站
            item['site'] = "财联社"
            # 出错的描述
            item['desc'] = '响应错误'
            # 代码报出的错误
            item['exception'] = ''
            yield item
