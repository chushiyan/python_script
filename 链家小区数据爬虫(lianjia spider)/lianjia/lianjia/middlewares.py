# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

# 随机的User-Agent

from lianjia import settings

class RandomUserAgent(object):
    def process_request(self, request, spider):
        print('<<<<<<<<<< 进入随机UA  >>>>>>>>>>')
        request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)


