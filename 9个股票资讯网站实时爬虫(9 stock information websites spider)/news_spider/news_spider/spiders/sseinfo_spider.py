# -*- coding: utf-8 -*-
'''
上证e互动爬虫

     author:MingKnight
     date:2019-5-17
     version:1.0.0
'''
import scrapy
from news_spider.items import NewsItem, ErrorItem, QuestionsAnswersItem
import time, datetime
import json
from news_spider import settings
import random
import re
import urllib.parse


class SseinfoSpiderSpider(scrapy.Spider):
    name = 'sseinfo_spider'
    allowed_domains = ['sseinfo.com']
    custom_settings = {
        'LOG_FILE': name + '.log'
    }

    # start_urls = ['http://sseinfo.com/']

    def start_requests(self):
        base_url = 'http://sns.sseinfo.com/ajax/feeds.do?type=11&pageSize=10&lastid=-1&show=1&page=1'
        while True:
            time.sleep(settings.global_sleep_time)
            yield scrapy.Request(url=base_url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):

        if response.status == 200:
            divs = response.xpath('//div[@class="m_feed_item"]')
            if divs is None or len(divs) == 0:
                item = ErrorItem()
                item['code'] = 801
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的网站
                item['site'] = "上证e互动"
                # 出错的描述
                item['desc'] = '未找到html元素'
                # 代码报出的错误
                item['exception'] = ''
                return item
            try:
                for div in divs:
                    q_a = div.xpath('.//div[@class="m_feed_txt"]/text()').getall()
                    # 得到的是问题 、回答 、再加一个''组成的数组

                    item = QuestionsAnswersItem()
                    item['source'] = 'sseinfo'

                    temp = div.xpath('.//div[@class="m_feed_txt"]/a/text()').get()  # 如：:中国化学(601117)
                    item['stockcode'] = re.findall('\d{6}', temp)[0]

                    # temp_list = div.xpath('.//div[@class="m_feed_from"]/span/text()').getall()
                    # 得到的是问题的时间和回答的时间组成的数组
                    # 如：
                    # 04月08日 18:35
                    # 16分钟前
                    #也可能是：
                    # 04月08日 18:35
                    # 1小时前
                    #
                    # num = int(re.findall('\d+', temp_list[1])[0])
                    #
                    # d = ''
                    # if '小时' in temp_list[1]: # 提取小时数
                    #     d = datetime.datetime.now() - datetime.timedelta(hours=num)
                    # if '分钟' in temp_list[1]: # 提取分钟数
                    #     d = datetime.datetime.now() - datetime.timedelta(minutes=num)
                    #
                    # t = d.timetuple()
                    # timeStamp = int(time.mktime(t))
                    #
                    # item['timestamp'] = timeStamp
                    item['pubDate'] = ''
                    item['question'] = q_a[1]
                    item['answer'] = q_a[2]
                    yield item

            except Exception as e:
                item = ErrorItem()
                item['code'] = 802
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的网站
                item['site'] = "上证e互动"
                # 出错的描述
                item['desc'] = '解析html标签错误'
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
            item['site'] = "上证e互动"
            # 出错的描述
            item['desc'] = '响应错误'
            # 代码报出的错误
            item['exception'] = ''
            yield item
