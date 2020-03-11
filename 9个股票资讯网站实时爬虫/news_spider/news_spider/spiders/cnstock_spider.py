# -*- coding: utf-8 -*-
import scrapy
from news_spider.items import NewsItem, ErrorItem
import time, datetime
import json
from news_spider import settings
import random
import re


class CnstockSpiderSpider(scrapy.Spider):
    name = 'cnstock_spider'
    allowed_domains = ['news.cnstock.com']
    custom_settings = {
        'LOG_FILE': name + '.log',
        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 100,
        'CONCURRENT_ITEMS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
        'CONCURRENT_REQUESTS_PER_IP': 16,
        'DOWNLOAD_TIMEOUT': 0.6,
    }

    # start_urls = ['http://news.cnstock.com/']

    def start_requests(self):
        base_url = 'http://news.cnstock.com/bwsd/index.html'
        while True:
            time.sleep(settings.global_sleep_time)
            yield scrapy.Request(url=base_url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        if response.status == 200:

            lis = response.xpath('//ul[@class="nf-list"]/li')
            if lis is None or len(lis) == 0:
                item = ErrorItem()
                item['code'] = 801
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的网站
                item['site'] = "上证快讯"
                # 出错的描述
                item['desc'] = '未找到html元素'
                # 代码报出的错误
                item['exception'] = ''
                return item
            try:
                # 日期：2019年05月16日
                # riqi = response.xpath('//div[@class="nf-head"]/p/text()').get().strip()
                for li in lis:
                    item = NewsItem()
                    item['source'] = "cnstock"
                    # temp = li.xpath('./p[1]/text()').get()  # 如：20:30
                    # temp = riqi + temp  # 2019年05月16日20:30
                    #
                    # d = datetime.datetime.strptime(temp, "%Y年%m月%d日%H:%M")
                    # t = d.timetuple()
                    # timeStamp = int(time.mktime(t))
                    #
                    # item['pubDate'] = timeStamp

                    item['pubDate'] = ''
                    title_conent = li.xpath('./p[2]/a/text()').get()

                    # 如：
                    '''
                    【压垮乐视网的最后一根稻草竟然是它！】15日，进入暂停上市状态第三天的乐视网披露，因乐视体育经营不利导致增资协议中的对赌条款失败，乐视体育股东之一的前海思拓提出的涉及回购融资股权的仲裁申请，得到了北京仲裁委员会的支持。
                    '''
                    item['title'] = (re.findall('【.*】', title_conent)[0]).replace('【', '').replace('】', '')
                    item['content'] = re.findall('】.*', title_conent)[0].replace('】', '')


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
                item['site'] = "上证快讯"
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
            item['site'] = "上证快讯"
            # 出错的描述
            item['desc'] = '响应错误'
            # 代码报出的错误
            item['exception'] = ''
            yield item
