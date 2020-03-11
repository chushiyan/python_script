# -*- coding: utf-8 -*-
import scrapy
from alibaba.items import ProviderContactItem
import csv
import re
import time
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains


class ProviderDetailSpider(scrapy.Spider):
    name = 'provider_detail'
    allowed_domains = ['1688.com']

    # start_urls = ['http://1688.com/']

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.set_window_size(1920, 3000)
        self.wait = WebDriverWait(self.driver, 10)

    def start_requests(self):

        self.login()
        reqs = []
        # login_url = r'https://www.1688.com/'
        # reqs.append(scrapy.Request(url=login_url, dont_filter=True))
        with open("alibaba/spiders/alibaba_provider.csv", "r", encoding='utf-8') as f:
            csvLines = csv.reader(f)
            print(type(csvLines))
            for csvLine in csvLines:  # csvLine 是一个列表
                url = csvLine[0]
                item = ProviderContactItem()
                item['url'] = url
                url = url + '/page/contactinfo.htm'
                print(url)
                reqs.append(scrapy.Request(url=url, meta={'item': item}, callback=self.parse_detail, dont_filter=True))
        return reqs

        # urls = ['https://0593ry.1688.com',
        #         'https://0662js.1688.com',
        #         'https://0663dongye.1688.com'
        #         ]
        #
        # for url in urls:
        #     item = ProviderContactItem()
        #     item['url'] = 'https://0593ry.1688.com'
        #     reqs.append(scrapy.Request(url=url+'/page/contactinfo.htm',meta={'item': item}, callback=self.parse_detail, dont_filter=True))
        # return reqs

    def login(self):
        login_url = r'https://www.1688.com/'
        self.driver.get(login_url)
        time.sleep(70)

    def parse_detail(self, response):
        item = response.meta['item']
        item['linkman'] = response.xpath('//div[@class="fd-clr"]/div/dl/dd/a/text()').get()

        temp = response.xpath('//div[@class="fd-clr"]/div/dl/dd/text()').getall()
        temp = ''.join(temp)
        item['linkman_position'] = temp

        div = response.xpath('//div[@class="contcat-desc"]')
        if div is None:
            print("未找到联系方式所在div")
            return

        contact_list = []
        for dl in div.xpath('./dl'):
            dl_list = []
            dt_text = dl.xpath('./dt/text()').get()
            dd_text = dl.xpath('./dd/text()').get()
            dl_list.append(dt_text)
            dl_list.append(dd_text)
            contact_list.append(dl_list)

        for dl_list in contact_list:
            dl_text = None
            dd_text = None
            try:
                dl_text = dl_list[0]
                dd_text = dl_list[1]
            except Exception as e:
                print(e)
            if (dl_text is None) or (dd_text is None):
                continue

            if '电&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;话' in dl_text:
                item['telephone'] = dd_text

            if '移动电话' in dl_text:
                item['mobile_phone'] = dd_text

            if '传' in dl_text:
                item['fax'] = dd_text


        # item['telephone'] = div.xpath('./dl[1]/dd/text()').get()
        #
        # item['mobile_phone'] = div.xpath('./dl[2]/dd/text()').get()
        #
        # item['fax'] = div.xpath('./dl[3]/dd/text()').get()
        yield item

    def closed(self, spider):
        print("<<<<<<<<<<<<<<<<<< spider closed >>>>>>>>>>>>>>>>>>")
        self.driver.close()
