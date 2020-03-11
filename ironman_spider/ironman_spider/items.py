# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RaceNameItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()


class ResultItem(scrapy.Item):
    name = scrapy.Field()
    country = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    div_rank = scrapy.Field()
    gender_rank = scrapy.Field()
    overall_rank = scrapy.Field()
    swim_time = scrapy.Field()
    bike_time = scrapy.Field()
    run_time = scrapy.Field()
