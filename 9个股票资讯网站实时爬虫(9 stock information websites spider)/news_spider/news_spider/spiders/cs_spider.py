# -*- coding: utf-8 -*-
'''
 用于爬取中证网的爬虫
 author:MingKnight
 date:2019-5-16 14:44:44
 versoin: 1.0.0
'''
import scrapy
from news_spider.items import NewsItem, ErrorItem
import time, datetime
import json
from news_spider import settings
import random


class CsSpiderSpider(scrapy.Spider):


    name = 'cs_spider'
    allowed_domains = ['cs.com.cn']
    custom_settings = {
        'LOG_FILE': name + '.log'
    }

    def start_requests(self):
        base_url = 'http://www.cs.com.cn/sylm/jsbd/index.shtml'
        while True:
            time.sleep(settings.global_sleep_time)
            yield scrapy.Request(url=base_url, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        if response.status == 200:
            lis = response.xpath('/html/body/div/div/ul/li')
            if lis is None or len(lis) == 0:
                item = ErrorItem()
                item['code'] = 801
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                item['date'] = time.time()
                # 出错的网站
                item['site'] = "中证网"
                # 出错的描述
                item['desc'] = '未找到html元素'
                # 代码报出的错误
                item['exception'] = ''
                return item
            try:
                for li in lis:
                    item = NewsItem()
                    item['source'] = "cs"

                    # temp = li.xpath('./span/text()').get().strip()  # 19-05-16 18:43
                    # temp = '20' + temp
                    # d = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M")
                    # t = d.timetuple()
                    # timeStamp = int(time.mktime(t))
                    #
                    # item['pubDate'] = timeStamp

                    item['pubDate'] =''
                    item['title'] = li.xpath('./a/text()').get()
                    url = r'http://www.cs.com.cn/sylm/jsbd/' + li.xpath('./a/@href').get()

                    yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_item, dont_filter=True)

            except Exception as e:
                item = ErrorItem()
                item['code'] = 802
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的网站
                item['site'] = "中证网"
                # 出错的描述
                item['desc'] = '解析html元素错误'
                # 代码报出的错误
                item['exception'] =  str(e)
                yield item

    def parse_item(self, response):
        if response.status == 200:
            try:
                item = response.meta['item']
                item['content'] = response.xpath('//div[@class="article-t hidden"]/p/text()').get()
                # TODO
                item['isRed'] = 0
                yield item
            except Exception as e:
                item = ErrorItem()
                item['code'] = 802
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的网站
                item['site'] = "中证网"
                # 出错的描述
                item['desc'] = '解析html元素错误'
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
            # 出错的网站
            item['site'] = "中证网"
            # 出错的描述
            item['desc'] = '响应错误'
            # 代码报出的错误
            item['exception'] = ''
            yield item
