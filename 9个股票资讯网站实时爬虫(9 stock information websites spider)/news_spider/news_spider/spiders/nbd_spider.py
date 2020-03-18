# -*- coding: utf-8 -*-
import scrapy
from news_spider.items import NewsItem, ErrorItem
import time, datetime
import json
from news_spider import settings
import random


class NbdSpiderSpider(scrapy.Spider):
    name = 'nbd_spider'
    allowed_domains = ['nbd.com.cn']
    custom_settings = {
        'LOG_FILE': name + '.log'
    }

    def start_requests(self):
        base_url = 'http://live.nbd.com.cn/'

        while True:
            time.sleep(settings.global_sleep_time)
            yield scrapy.Request(url=base_url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        if response.status == 200:
            lis = response.xpath('//ul[@class="live-list"]/li')
            if lis is None or len(lis) == 0:
                item = ErrorItem()
                item['code'] = 801
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的网站
                item['site'] = "每经网"
                # 出错的描述
                item['desc'] = '未找到html元素'
                # 代码报出的错误
                item['exception'] = ''
                return item

            try:
                riqi = response.xpath('//p[@class="live"]/span/text()').getall() # 如：2019年05月20日
                date = ''
                for temp in riqi:
                    if "年" in temp:
                        date = temp.replace("\n", "").replace("\n\r", "").replace("\r\n", "").replace("\r", "").strip()
                        break

                for li in lis:
                    i = NewsItem()
                    i['source'] = "nbd"

                    timeStamp = ''
                    try:
                        temp = (li.xpath('./div[@class="li-title"]/p/span/text()').get())
                        # 如：17:44:42

                        temp = temp.replace("\n", "").replace("\n\r", "").replace("\r\n", "").replace("\r", "").strip()

                        temp = date + temp  # 如：2019年05月16日 18:26:27

                        d = datetime.datetime.strptime(temp, "%Y年%m月%d日%H:%M:%S")
                        t = d.timetuple()
                        timeStamp = time.mktime(t)
                    except Exception as e:
                        print(e)
                        i['pubDate'] = ""
                    else:
                        i['pubDate'] = timeStamp

                    i['title'] = ""
                    i['content'] = li.xpath('./div[@class="li-text"]/a/text()').get()
                    # TODO
                    i['isRed'] = 0
                    yield i
            except Exception as e:
                item = ErrorItem()
                item['code'] = 802
                # 出错的页面
                item['url'] = response.url
                # 出错的时间
                # item['timestamp'] = time.time()
                # 出错的网站
                item['site'] = "每经网"
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
            item['site'] = "每经网"
            # 出错的描述
            item['desc'] = '响应错误'
            # 代码报出的错误
            item['exception'] = ''
            yield item
