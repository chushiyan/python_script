# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoQuItem(scrapy.Item):
    # 城市
    city = scrapy.Field()

    # 区
    district = scrapy.Field()

    # 区url
    district_url = scrapy.Field()



    # 街/路
    load = scrapy.Field()

    # 小区名称
    community = scrapy.Field()

    # 小区详情页
    community_url = scrapy.Field()

    # 房屋总数
    house_totol = scrapy.Field()

    # 物业公司
    property_companies = scrapy.Field()

    # 开发商
    developer = scrapy.Field()
