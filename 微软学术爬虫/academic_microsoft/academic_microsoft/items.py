# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlockChainItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    url = scrapy.Field()

    Pub_Title = scrapy.Field()

    Year = scrapy.Field()

    Pub_Outlet = scrapy.Field()

    Citation_Count = scrapy.Field()

    # 摘要
    Abstract = scrapy.Field()

    # 字典：  作者名：学校
    Author= scrapy.Field()
    # Author1_Insttute = scrapy.Field()

    # Author2 = scrapy.Field()
    # Author2_Insttute = scrapy.Field()
    #
    # Author3 = scrapy.Field()
    # Author3_Insttute = scrapy.Field()
    #
    # Author4 = scrapy.Field()
    # Author4_Insttute = scrapy.Field()
    #
    # Author5 = scrapy.Field()
    # Author5_Insttute = scrapy.Field()
    #
    # Author6 = scrapy.Field()
    # Author6_Insttute = scrapy.Field()



    # 数组
    Tag = scrapy.Field()



