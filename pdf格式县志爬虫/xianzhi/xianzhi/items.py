# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XianzhiItem(scrapy.Item):
    index = scrapy.Field()

    content = scrapy.Field()

    title = scrapy.Field()

    father = scrapy.Field()

    kw = scrapy.Field()

    url = scrapy.Field()

    pdf_url = scrapy.Field()