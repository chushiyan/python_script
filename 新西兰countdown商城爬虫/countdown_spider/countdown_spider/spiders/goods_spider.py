# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from countdown_spider.items import GoodsItem

from countdown_spider import settings
import datetime, time


class GoodsSpiderSpider(CrawlSpider):
    name = 'goods_spider'
    allowed_domains = ['shop.countdown.co.nz']
    start_urls = ['http://shop.countdown.co.nz/']

    rules = (

        Rule(LinkExtractor(allow=r'/shop/browse/.*'), follow=True),
        # '/shop/browse/bakery?page=2'
        # Rule(LinkExtractor(allow=r'/shop/browse/.*\?page=\d+'), follow = True),
        Rule(LinkExtractor(allow=r'/shop/productdetails\?.*'), callback='parse_item', follow=False)
    )

    def parse_item(self, response):
        item = GoodsItem()
        # item['date'] = time.time()
        item['date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item['title'] = response.xpath('//h1/text()').get()
        item['url'] = response.url

        # $19.00 ea
        price = response.xpath(
            "//span[contains(@class,'product-price')]/span[contains(@class,'price')][1]/text()").get()
        if price is None:
            price = response.xpath('//span[contains(@class,"club-price-wrapper")]/text()').get()
        if price is not None:
            price = price.replace('\r\n', ' ').replace('\t', ' ').strip()
            item['price'] = price.split(' ')[0]

            item['unitOfMeasurement'] = price.split(' ')[-1]

        # item['price'],item['unitOfMeasurement'] = price.split('&nbsp;')
        item['volumeSize'] = response.xpath('//h1/span/text()').get()
        # item['unitOfMeasurement'] = item['title'].split(' ')
        # item['unitOfMeasurement'] = price.split('&nbsp;')[-1]
        return item
