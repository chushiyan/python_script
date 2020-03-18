# -*- coding: utf-8 -*-
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import time


class SeleniumMiddleware(object):

    def process_request(self, request, spider):
        driver = spider.driver
        wait = spider.wait
        if request.url != r'https://www.1688.com/':
            print('----------------------', request.url, '----------------------')

            print('.....the request inter selenium......')
            try:
                driver.get(request.url)
                time.sleep(5)
            except TimeoutException as e:
                print('.....selenium timeout....')

            html_response = HtmlResponse(url=driver.current_url, body=driver.page_source,
                                         encoding="utf-8", request=request)
            return html_response
