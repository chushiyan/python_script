# -*- coding: utf-8 -*-
import scrapy
from calbar_spider.items import LawyerItem
import re


class LawyerspiderSpider(scrapy.Spider):
    name = 'lawyerspider'
    allowed_domains = ['calbar.ca.gov']

    start_urls = [
        'http://members.calbar.ca.gov/fal/LicenseeSearch/QuickSearch?ResultType=0&SearchType=0&SoundsLike=False#searchlink']

    # start_urls = [
    #     'http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName=&FirstNameOption=b&FirstName=&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=&State=&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken=7']

    def parse(self, response):
        requests = []
        # langage_base_url = r'http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName=&FirstNameOption=b&FirstName=&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=&State=&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken={}'
        # langage_options = response.xpath('//select[@id="LanguageSpoken"]/option')
        # print('------- the number of langage options : ', len(langage_options), ' --------')
        # for option in langage_options:
        #     value = option.xpath('./@value').get()
        #     print(value)
        #     if not value:
        #         continue
        #     url = langage_base_url.format(value)
        #     print(url)
        #     requests.append(scrapy.Request(url=url, callback=self.parse_table, dont_filter=True))
        #
        # state_base_url = r'http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName=&FirstNameOption=b&FirstName=&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=&State={}&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken='
        # state_options = response.xpath('//select[@id="State"]/option')
        # print('------- the number of langage options : ', len(langage_options), ' --------')
        # for option in state_options:
        #     value = option.xpath('./@value').get()
        #     # print(value)
        #     if not value:
        #         continue
        #     url = state_base_url.format(value)
        #     print(url)
        #     requests.append(scrapy.Request(url=url, callback=self.parse_table, dont_filter=True))


        # r'http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName=a&FirstNameOption=b&FirstName=a&MiddleNameOption=b&MiddleName=a&FirmNameOption=b&FirmName=a&CityOption=b&City=&State=&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken=#searchlink'
        # name_base_url = r'http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName={0}&FirstNameOption=b&FirstName={1}&MiddleNameOption=b&MiddleName={2}&FirmNameOption=b&FirmName=&CityOption=b&City=&State=&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken=#searchlink'
        name_base_url = r'http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName={0}&FirstNameOption=b&FirstName={1}&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=&State=&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken=#searchlink'

        list = [chr(i) for i in range(97, 123)]
        for char1 in list:
            for char2 in list:
                # for char3 in list:
                #     url = name_base_url.format(char1, char2, char3)
                url = name_base_url.format(char1, char2)
                requests.append(scrapy.Request(url=url, callback=self.parse_table, dont_filter=True))
        return requests

    def parse_table(self, response):
        # def parse(self, response):
        table = response.xpath('//div[@id="moduleAttorneySearchList"]//table')
        if table is None:
            print('No table found in the page : ', response.url)

        for tr in table.xpath('./tbody/tr'):

            item = LawyerItem()

            link = tr.xpath('.//a/@href').get()

            if link is not None:
                item['detail_url'] = r'http://members.calbar.ca.gov' + link
                print(item['detail_url'])
            else:
                print('..... failed to extract href  ......')

            name = tr.xpath('.//a/text()').get()
            if name is not None:
                name = re.sub(' +', ' ', name)
                item['name'] = name.strip()

            license_status = tr.xpath('./td[2]/text()').get()
            if license_status is not None:
                item['license_status'] = license_status.strip()

            number = tr.xpath('./td[3]/text()').get()
            if number is not None:
                item['number'] = number.strip()

            city = tr.xpath('./td[4]/text()').get()
            if city is not None:
                item['city'] = city.strip()

            admission_date = tr.xpath('./td[5]/text()').get()
            if admission_date is not None:
                item['admission_date'] = admission_date.strip()

            # yield item
            yield scrapy.Request(url=item['detail_url'], meta={'item': item}, callback=self.parse_detail,
                                 dont_filter=True)

    def parse_detail(self, response):

        item = response.meta['item']

        # print('-------- spider -------：', item)

        # item['email'] =  response.meta['email']

        div_detail = response.xpath('//div[@id="moduleMemberDetail"]')
        if div_detail is None:
            print("No detail's div found in the page : ", response.url)

        text_list = div_detail.xpath('.//text()').getall()
        # print(text_list)

        if text_list is not None:
            for text in text_list:
                if "Address" in text:
                    item['address'] = text.split(':')[-1].strip()

                if "County" in text:
                    item['county'] = text.split(':')[-1].strip()

                if "Phone Number" in text:
                    item['phone_number'] = text.split(':')[-1].strip()

                if "Fax Number" in text:
                    item['fax_number'] = text.split(':')[-1].strip()

                if "Law School" in text:
                    item['law_school'] = text.split(':')[-1].strip()

        item['cla_sections'] = []
        lis = div_detail.xpath('.//table//tbody/tr[1]/td[2]/ul/li')
        print(lis)
        if lis is not None:
            for li in lis:
                text = li.xpath('./a/text()').get()
                if text is not None:
                    text = text.strip()
                    text = re.sub(' +', ' ', text)
                    item['cla_sections'].append(text)

        item['certified_legal_specialty'] = []
        lis = div_detail.xpath('.//table/tbody/tr/td[2]/ul/li')

        if lis is not None:
            for li in lis:
                text = li.xpath('./text()').get()
                if text is not None:
                    text = text.strip()
                    text = re.sub(' +', ' ', text)
                    item['certified_legal_specialty'].append(text)

        yield item
