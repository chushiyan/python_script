# -*- coding: utf-8 -*-
import scrapy
from news_spider.items import NewsItem, ErrorItem
import json


class TestSpiderSpider(scrapy.Spider):
    name = 'test_spider'
    allowed_domains = ['httpbin.org']
    # start_urls = ['http://httpbin.org/']
    custom_settings = {
        'LOG_FILE': name + '.log'
    }


    def start_requests(self):

        while True:
            url = 'http://httpbin.org/get'
            yield scrapy.Request(url=url,callback=self.parse_item, dont_filter=True )


    def parse_item(self, response):

        if response.status == 200:
            try:
                data = json.loads('['+response.body.decode()+']')
                print(data)
            except Exception as e:
                print(e)
                item = ErrorItem()
                item['code'] = response.status
                # 出错的页面
                item['url'] = 901
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的url
                item['site'] = "httpbin"
                # 出错的描述
                item['desc'] = '响应的json数据错误'
                # 代码报出的错误
                item['exception'] =  str(e)
                return item
            else:
                try:
                    for item in data:
                        i = NewsItem()
                        i['source'] = "httpbin"
                        # print(item)
                        i['pubDate'] = ""
                        i['title'] = ""
                        i['content'] = item['origin']
                        yield i
                except Exception as e:
                    item = ErrorItem()
                    item['code'] = response.status
                    # 出错的页面
                    item['url'] = 902
                    # 出错的时间
                    # item['timestamp'] = time.time()
                    # 出错的url
                    item['site'] = "httpbin"
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
            item['site'] = "httpbin"
            # 出错的描述
            item['desc'] = '响应错误'
            # 代码报出的错误
            item['exception'] = ''
            yield item

