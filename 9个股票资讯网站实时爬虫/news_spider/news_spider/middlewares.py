# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import random
import base64
from news_spider import settings
from . import db
import random

from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
import time, datetime


class ProcessAllExceptionMiddleware(object):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    # def process_response(self, request, response, spider):
    #     # 捕获状态码为40x/50x的response
    #     if str(response.status).startswith('4') or str(response.status).startswith('5') or str(
    #             response.status).startswith('3'):
    #         print('报错的是4和5 3开头的重新请求')
    #         return request
    #     if 'forbidden' in response.url:
    #         return request
    #     return response

    def process_exception(self, request, exception, spider):
        # 捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            # 在日志中打印异常类型
            print("")
            print('######### %s  ' % (exception), datetime.datetime.now(), '#########')
            print("")
            # spider.logger.warning('###############  %s  ###############' % (exception))
            return request


# 随机的User-Agent
class RandomUserAgent(object):
    def process_request(self, request, spider):
        # TODO 部署后需要删除
        # if spider.name == "test_spider":
        #     request.headers['Referer'] = "http://httpbin.org/"
        #     request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)

        if spider.name == "cls_spider":
            # print('<<<<<<<<<<<<<<<<<<<<<<    >>>>>>>>>>>>>>>>>>>>>>>>')
            # request.headers['Host'] = "www.cls.cn"
            # request.headers['If-None-Match'] = 'W/"3f-WG/1HjmC3FTHAG8QCCJGb5w1iSY"'
            # request.headers['authorization'] = "Bearer undefined"
            request.headers['Connection'] = "close"
            request.headers['Referer'] = "https://www.cls.cn/"
            request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)

        if spider.name == "cninfo_spider":
            # print('<<<<<<<<<<<<<<<<<<<<<<    >>>>>>>>>>>>>>>>>>>>>>>>')
            # request.headers['Host'] = "irm.cninfo.com.cn"
            request.headers['x-requested-with'] = "XMLHttpRequest"
            request.headers['Connection'] = "close"
            request.headers['Referer'] = "http://irm.cninfo.com.cn/"
            request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)

        if spider.name == "cnstock_spider":
            # print('<<<<<<<<<<<<<<<<<<<<<<    >>>>>>>>>>>>>>>>>>>>>>>>')
            # request.headers['Host'] = "news.cnstock.com"
            request.headers['Connection'] = "close"
            request.headers['Referer'] = "http://news.cnstock.com/bwsd/index.html"
            request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)

        if spider.name == "cs_spider":
            # print('<<<<<<<<<<<<<<<<<<<<<<    >>>>>>>>>>>>>>>>>>>>>>>>')
            # request.headers['Host'] = "www.cs.com.cn"
            request.headers['Connection'] = "close"
            request.headers['Referer'] = "http://www.cs.com.cn/sylm/jsbd/index.shtml"
            request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)

        if spider.name == "egs_spider":
            # print('<<<<<<<<<<<<<<<<<<<<<<    >>>>>>>>>>>>>>>>>>>>>>>>')
            request.headers['x-requested-with'] = "XMLHttpRequest"
            request.headers['Referer'] = "http://egs.stcn.com/news"
            request.headers['Connection'] = "close"
            request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)

        if spider.name == "nbd_spider":
            # print('<<<<<<<<<<<<<<<<<<<<<<    >>>>>>>>>>>>>>>>>>>>>>>>')
            # request.headers['Host'] = "live.nbd.com.cn"
            request.headers['Referer'] = "http://live.nbd.com.cn/"
            request.headers['Connection'] = "close"
            request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)

        if spider.name == "sseinfo_spider":
            # print('<<<<<<<<<<<<<<<<<<<<<<    >>>>>>>>>>>>>>>>>>>>>>>>')
            # request.headers['Host'] = "sns.sseinfo.com"
            # request.headers['If-None-Match'] = 'W/"3f-WG/1HjmC3FTHAG8QCCJGb5w1iSY"'
            # request.headers['authorization'] = "Bearer undefined"
            request.headers['Connection'] = "close"
            request.headers['Referer'] = "http://sns.sseinfo.com/index.do"
            request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)

        if spider.name == "xuangubao_spider":
            # print('<<<<<<<<<<<<<<<<<<<<<<    >>>>>>>>>>>>>>>>>>>>>>>>')
            # request.headers['Origin'] = "https://xuangubao.cn"
            request.headers['Connection'] = "close"
            request.headers['Referer'] = "https://xuangubao.cn/"
            request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)

        if spider.name == "yicai_spider":
            # print('<<<<<<<<<<<<<<<<<<<<<<    >>>>>>>>>>>>>>>>>>>>>>>>')
            request.headers['x-requested-with'] = "XMLHttpRequest"
            request.headers['Connection'] = "close"
            request.headers['Referer'] = "https://www.yicai.com/brief"
            request.headers['User-Agent'] = random.choice(settings.USER_AGENT_LIST)


class RandomProxy(object):
    def __init__(self):
        # self.client = db.RedisClient(host='47.107.227.145', password= 'diF_76_daU($#dKi)*7&1285#@',port=6379)
        self.client = db.RedisClient(host='localhost', password='diF_76_daU($#dKi)*7&1285#@', port=6379)
    def process_request(self, request, spider):
        # TODO 部署后需要修改
        # proxy = random.choice(settings.PROXIES)
        # request.meta['proxy'] = "http://" + proxy['ip_port']

        # ip = '59.38.14.173'
        # proxy = ip + ':3435'
        # request.meta['proxy'] = 'http://'+proxy
        # print('<<<<<<<<<<< %s >>>>>>>>>>>'%proxy,datetime.datetime.now())

        try:
            proxy = self.client.random()
            print('<<<<<<<<<< %s >>>>>>>>>>' % proxy)
            request.meta['proxy'] = "http://" + proxy
        except Exception as e:
            print(e)


class NewsSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class NewsSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
