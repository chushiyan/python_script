# -*- coding: utf-8 -*-
'''
互动易爬虫
通过http://irm.cninfo.com.cn/ircs/index/search 加上post参数 获取数据
     author:MingKnight
     date:2019-5-17
     version:1.0.0
'''
import scrapy
from news_spider.items import NewsItem, ErrorItem,QuestionsAnswersItem
import time, datetime
import json
from news_spider import settings
import random
import re
import urllib.parse


class CninfoSpiderSpider(scrapy.Spider):
    name = 'cninfo_spider'
    allowed_domains = ['cninfo.com.cn']
    # start_urls = ['http://cninfo.com.cn/']
    custom_settings = {
        'LOG_FILE': name + '.log'
    }

    def start_requests(self):
        base_url = 'http://irm.cninfo.com.cn/ircs/index/search'
        while True:
            time.sleep(settings.global_sleep_time)
            yield scrapy.FormRequest(
                url=base_url,
                formdata={
                    'pageNo': '1',
                    'pageSize': '1',
                    'searchTypes': '1,11,',
                    'keyWord': '',
                    'market': '',
                    'industry': '',
                    'stockCode': ''
                },
                callback=self.parse_item,
                dont_filter=True
            )

    def parse_item(self, response):

        if response.status == 200:
            try:
                data_list = json.loads('[' + response.body.decode() + ']')
                # print(data_list)
            except Exception as e:
                print(e)
                item = ErrorItem()
                item['code'] = 800
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的url
                item['source'] = "互动易"
                # 出错的描述
                item['desc'] = '响应的json数据错误'
                # 代码报出的错误
                item['exception'] = e
                yield item
            else:
                try:
                    for data in data_list[0]["results"]:
                        item = QuestionsAnswersItem()
                        item['source'] = 'cninfo'
                        item['stockcode'] =data['stockCode']
                        item['pubDate'] = data['pubDate']
                        item['question'] = data['mainContent']
                        item['answer'] =data['attachedContent']

                        yield item
                except Exception as e:
                    item = ErrorItem()
                    item['code'] = 902
                    # 出错的页面
                    item['url'] = response.url
                    # 出错的时间
                    # item['timestamp'] = time.time()
                    # 出错的url
                    item['source'] = "cninfo"
                    # 出错的描述
                    item['desc'] = '解析json数据错误'
                    # 代码报出的错误
                    item['exception'] = e
                    yield item
        else:
            item = ErrorItem()
            item['code'] = response.status
            # 出错的页面
            item['url'] = response.url
            # 出错的时间
            # item['timestamp'] = time.time()
            # 出错的url
            item['source'] = "互动易"
            # 出错的描述
            item['desc'] = '响应错误'
            # 代码报出的错误
            item['exception'] = ''
            yield item
