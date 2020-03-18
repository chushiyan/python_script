# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    flag = 1
    # flag = scrapy.Field()
    source = scrapy.Field()
    pubDate = scrapy.Field()
    timestamp = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    # 1 是red  , 0 不是
    isRed = scrapy.Field()


class QuestionsAnswersItem(scrapy.Item):
    flag = 2
    source = scrapy.Field()
    pubDate = scrapy.Field()
    timestamp = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()
    stockcode = scrapy.Field()


class ErrorItem(scrapy.Item):
    flag = 3
    # 错误码：如 302,404,500代表请求错误
    # 自定义：
    # 801 ： 未找到html元素
    # 802：  解析html标签错误
    # 901：  响应的json数据错误
    # 902:   解析json数据错误
    code = scrapy.Field()

    # 出错的页面
    url = scrapy.Field()

    # 出错的时间，是时间戳
    timestamp = scrapy.Field()

    # 出错的url
    site = scrapy.Field()

    # 出错的描述
    desc = scrapy.Field()

    # 代码报出的错误
    exception = scrapy.Field()
