# -*- coding: utf-8 -*-
'''
选股宝爬虫
使用的是ajax请求
     author:MingKnight
     date:2019-5-16
     version:1.0.0
'''
import scrapy
from news_spider.items import NewsItem, ErrorItem
import time, datetime
import json
from news_spider import settings
import random
import re


class XuangubaoSpiderSpider(scrapy.Spider):
    name = 'xuangubao_spider'
    allowed_domains = ['xuangubao.cn']
    start_urls = ['http://xuangubao.cn/']
    custom_settings = {
        'LOG_FILE': name + '.log'
    }

    def start_requests(self):
        # 原本的接口：
        # https://api.xuangubao.cn/api/pc/msgs?subjids=9,10,723,35,469,821&limit=30&tailmark=1558050675&msgIdMark=472205
        # https://api.xuangubao.cn/api/pc/msgs?subjids=9,10,723,35,469,821&limit=30&tailmark=1558051691&msgIdMark=472219
        # https://api.xuangubao.cn/api/pc/msgs?subjids=9,10,723,35,469,821&limit=30&tailmark=1558042490&msgIdMark=472161

        base_url = 'https://api.xuangubao.cn/api/pc/msgs?subjids=9,10,723,35,469,821&limit=1'
        while True:
            time.sleep(settings.global_sleep_time)
            # self.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)
            yield scrapy.Request(url=base_url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):

        if response.status == 200:
            try:
                # 不是格式正确的json,一前一后需要加上'[' ']'，
                data_list = json.loads('[' + response.body.decode() + ']')
                # print(data_list)
            except Exception as e:
                # print(e)
                item = ErrorItem()
                item['code'] = 901
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的url
                item['site'] = "选股宝"
                # 出错的描述
                item['desc'] = '响应的json数据错误'
                # 代码报出的错误
                item['exception'] =  str(e)
                yield item
            else:
                try:
                    for data in data_list[0]["NewMsgs"]:
                        item = NewsItem()
                        # item['flag'] = 1
                        item['source'] = 'xuangubao'
                        item['pubDate'] = data['UpdatedAtInSec']
                        item['title'] = data['Title']
                        item['content'] = data['Summary']
                        # TODO
                        item['isRed'] = data['Impact']
                        yield item

                except Exception as e:
                    # print(e)
                    item = ErrorItem()
                    item['code'] = 902
                    # 出错的页面
                    item['url'] = response.url
                    # 出错的时间
                    # item['timestamp'] = time.time()
                    # 出错的url
                    item['site'] = "选股宝"
                    # 出错的描述
                    item['desc'] = '解析json数据错误'
                    # 代码报出的错误
                    item['exception'] =  str(e)
                    yield item

        else:
            item = ErrorItem()
            item['code'] = response.status
            # 出错的页面
            item['url'] = response.url
            # 出错的时间
            # item['timestamp'] = time.time()
            # 出错的url
            item['site'] = "选股宝"
            # 出错的描述
            item['desc'] = '响应错误'
            # 代码报出的错误
            item['exception'] = ''
            yield item
