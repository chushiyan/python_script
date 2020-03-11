# -*- coding: utf-8 -*-
import scrapy
from academic_microsoft.items import BlockChainItem
import re
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import time

class BlockchainSpider(scrapy.Spider):
    name = 'blockchain'
    allowed_domains = ['academic.microsoft.com']

    # start_urls = ['http://academic.microsoft.com/']
    def __init__(self):
        super().__init__(self)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.set_window_size(1920, 3000)
        self.wait = WebDriverWait(self.driver, 20)

    def start_requests(self):
        r'https://academic.microsoft.com/search?q=blockchain&f=&orderBy=0&skip=0&take=1'
        base_url = r'https://academic.microsoft.com/search?q=blockchain&f=&orderBy=0&skip={}&take=10'
        reqs = []
        for i in range(0,4990+1):
        # for i in range(0, 0 + 1):
            reqs.append(scrapy.Request(base_url.format(i * 10), callback=self.parse_item, dont_filter=True))
        return reqs

    def parse_item(self, response):

        print(response.url, '-------------------------')

        for div in response.xpath('//div[@class="paper"]'):
            link = div.xpath('./a[1]')
            print(link)
            item = BlockChainItem()
            item['url'] = 'https://academic.microsoft.com/' + link.xpath('./@href').get()
            item['Pub_Title'] = link.xpath('./@data-appinsights-title').get()

            item['Year'] = div.xpath('./a/span[@class="year"]/text()').get()

            item['Pub_Outlet'] = div.xpath('./a/span[@class="name"]/text()').get()

            temp = div.xpath('.//div[@class="paper-footer"]//a/text()').get()
            '''
            CITATIONS* (567)
            CITATIONS* (1,318)
            CITATIONS* (460)
            CITATIONS* (481)
            CITATIONS* (603)
            CITATIONS* (136)
            '''
            item['Citation_Count'] = re.findall('\(.+\)', temp)[0][1:-1]

            if item['url'] is not None:
                print(item['url'], '###########################')
                yield scrapy.Request(url=item['url'], meta={'item': item}, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):

        item = response.meta['item']

        print(response.url)

        item['Abstract'] = response.xpath('//div[@class="header"]/div[@class="name-section"]/p/text()').get()

        item['Author'] = []

        spans = response.xpath('//div[@class="name-section"]//ma-author-string-collection/span')

        try:
            if spans is not None:
                for span in spans:
                    info = []
                    name = span.xpath('./a[1]/text()').get()
                    school = span.xpath('./a[2]/@data-appinsights-key').get()
                    info.append(name)
                    info.append(school)
                    item['Author'].append(info)

        except Exception as e:
            print(e)

        item['Tag'] = response.xpath(
            '//div[@class="edp paper"]//div[@class="tag-cloud"]//div[@class="text"]/text()').getall()
        print(item)

        yield item

    def closed(self, spider):
        print("spider closed")
        self.driver.close()
