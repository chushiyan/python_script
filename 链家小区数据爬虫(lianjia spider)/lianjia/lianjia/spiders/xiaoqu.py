# -*- coding: utf-8 -*-
import json

import scrapy

from lianjia.items import XiaoQuItem


class XiaoquSpider(scrapy.Spider):
    name = 'xiaoqu'
    allowed_domains = ['lianjia.com']
    start_urls = [
        # "https://tj.lianjia.com/xiaoqu/heping/",
        # "https://tj.lianjia.com/xiaoqu/nankai/",
        # "https://tj.lianjia.com/xiaoqu/hexi/",
        # "https://tj.lianjia.com/xiaoqu/hebei/",
        # "https://tj.lianjia.com/xiaoqu/hedong/",
        # "https://tj.lianjia.com/xiaoqu/hongqiao/",
        # "https://tj.lianjia.com/xiaoqu/xiqing/",
        # "https://tj.lianjia.com/xiaoqu/beichen/",
        # "https://tj.lianjia.com/xiaoqu/dongli/",
        # "https://tj.lianjia.com/xiaoqu/jinnan/",
        # "https://tj.lianjia.com/xiaoqu/tanggu/",
        # "https://tj.lianjia.com/xiaoqu/kaifaqutj/",
        # "https://tj.lianjia.com/xiaoqu/wuqing/",
        # "https://tj.lianjia.com/xiaoqu/binhaixinqu/",
        # "https://tj.lianjia.com/xiaoqu/baodi/",
        "https://tj.lianjia.com/xiaoqu/jizhou/",
        # "https://tj.lianjia.com/xiaoqu/haihejiaoyuyuanqu/",
        # "https://tj.lianjia.com/xiaoqu/jinghai/"
    ]

    # 从页面提取分页总数， 因为分页相关标签是动态生成的
    def parse(self, response):
        # <div class="page-box house-lst-page-box" comp-module='page' page-url="/xiaoqu/heping/pg{page}"page-data='{"totalPage":22,"curPage":1}'></div>
        st = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').get()
        page_data = json.loads(st)
        totalPage = page_data["totalPage"]
        if totalPage is None:
            totalPage = 30
        reqs = []
        for i in range(1, totalPage + 1):
            # 'https://tj.lianjia.com/xiaoqu/heping/pg1/'
            list_url = response.url + "pg{}/".format(i)
            print(list_url)
            # yield scrapy.Request(url=list_url, callback=self.parse_list, dont_filter=True)
            reqs.append(scrapy.Request(url=list_url, callback=self.parse_list, dont_filter=True))
        return reqs

    def parse_list(self, response):
        li_list = response.xpath('//ul[@class="listContent"]/li')

        if not li_list:
            print(response.url)
            print("没有找到小区列表所在li，可能是不存在该页面或者响应了验证页面")
            return

        for li in li_list:
            item = XiaoQuItem()
            item['city'] = '天津'
            item['district'] = response.xpath('//div[@data-role="ershoufang"]/div/a[@class="selected"]/text()').get()
            item["community"] = li.xpath('.//div[@class="title"]/a/text()').get()
            item['community_url'] = li.xpath('.//div[@class="title"]/a/@href').get()
            item["load"] = li.xpath('.//div[@class="positionInfo"]/a[@class="bizcircle"]/text()').get()

            yield scrapy.Request(url=item['community_url'],
                                 meta={'item': item},
                                 callback=self.parse_detail,
                                 dont_filter=True)

    def parse_detail(self, response):

        item = response.meta["item"]

        item['property_companies'] = response.xpath(
            '//span[contains(text(),"物业公司")]/following-sibling::span[1]/text()').get()

        item['developer'] = response.xpath(
            '//span[contains(text(),"开发商")]/following-sibling::span[1]/text()').get()

        item['house_totol'] = response.xpath(
            '//span[contains(text(),"房屋总数")]/following-sibling::span[1]/text()').get()

        print()
        print(response.url)
        print(item)
        print()

        yield item
