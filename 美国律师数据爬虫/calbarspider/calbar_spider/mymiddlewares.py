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

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.set_window_size(1920, 7000)
        self.wait = WebDriverWait(self.driver, 10)

    def process_request(self, request, spider):

        if request.url.startswith(r'http://members.calbar.ca.gov/fal/Licensee/Detail'):
            item = request.meta['item']

            print('.....the request inter selenium......')
            try:
                self.driver.get(request.url)
            except TimeoutException as e:
                print('.....selenium timeout....')

            try:
                div_detail = self.wait.until(
                    expected_conditions.presence_of_element_located((By.ID, "moduleMemberDetail")))
            except TimeoutException as e:
                print(e)
            else:
                try:
                    p = self.driver.find_element_by_xpath('//*[@id="moduleMemberDetail"]/div[2]/p[6]')
                    print(p.text)
                except Exception as e:
                    print(e)
                else:
                    if p.text is not None:
                        email = p.text.split(':')[-1].strip()
                    else:
                        email = None
                    item['email'] = email

            html_response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source,
                                         encoding="utf-8", request=request)
            html_response.meta['item'] = item
            # print('-------- middle ware -------：',item)

            return html_response
