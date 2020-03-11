# -*- coding: utf-8 -*-
'''
第一财经爬虫
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


class YicaiSpiderSpider(scrapy.Spider):
    name = 'yicai_spider'
    allowed_domains = ['yicai.com']
    custom_settings = {
        'LOG_FILE': name + '.log'
    }

    # start_urls = ['https://www.yicai.com/brief/']

    def start_requests(self):

        # 原始的url ： ttps://www.yicai.com/api/ajax/getbrieflist?page=2&pagesize=20&type=0
        base_url = 'https://www.yicai.com/api/ajax/getbrieflist?page=2&pagesize=20&type=00'
        while True:
            time.sleep(settings.global_sleep_time)
            yield scrapy.Request(url=base_url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):

        if response.status == 200:
            try:
                data_list = json.loads(response.body.decode())
                # print(data_list)
            except Exception as e:
                print(e)
                item = ErrorItem()
                item['code'] = 800
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                item['timestamp'] = time.time()
                # 出错的url
                item['site'] = "第一财经"
                # 出错的描述
                item['desc'] = '响应的json数据错误'
                # 代码报出的错误
                item['exception'] =  str(e)
                yield item
            else:
                try:
                    for data in data_list:
                        item = NewsItem()
                        item['source'] = 'yicai'
                        date = data['datekey'] + " " + data['hm']  # 如：2019.05.16 20:43
                        # print('<<<<<<<<<<< ' + temp + ' >>>>>>>>>>>')
                        d = datetime.datetime.strptime(date, "%Y.%m.%d %H:%M")
                        t = d.timetuple()
                        item['pubDate'] = int(time.mktime(t))

                        # print(item)
                        title_conent = data['newcontent']

                        # 如：【传化智联：非公开发行股票方案到期失效】 传化智联5月16日晚间公告，公司于2017年度股东大会审议通过《关于公司非公开发行股票方案的议案》，因资本市场环境变化等因素，公司此次非公开发行股票事项尚未取得实质进展。目前，此次非公开发行股票方案到期自动失效。 ",
                        item['title'] = re.findall('【.*】', title_conent)[0].replace('【', '').replace('】', '')
                        item['content'] = re.findall('】.*', title_conent)[0].replace('】', '')

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
                    # 出错的url
                    item['site'] = "第一财经"
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
            item['site'] = "第一财经"
            # 出错的描述
            item['desc'] = '响应错误'
            # 代码报出的错误
            item['exception'] = ''
            yield item