# -*- coding: utf-8 -*-
import scrapy
import time
import re
from tennislink_usta_spider.items import TournamentItem


class TournamentSpider(scrapy.Spider):
    name = 'tournament'
    allowed_domains = ['tennislink.usta.com']

    start_urls = [
        r'https://tennislink.usta.com/Tournaments/Schedule/Search.aspx']

    def __init__(self):
        self.table_count = 0

    def parse(self, response):

        base_url = r'https://tennislink.usta.com/Tournaments/Schedule/SearchResults.aspx?' \
                   r'typeofsubmit=&Action=2&Keywords=&TournamentID=&SectionDistrict=&City=&' \
                   r'State={state}&Zip=&Month={month}&StartDate=&EndDate=&Day=&Year={year}&Division=&' \
                   r'Category=&Surface={surface}&OnlineEntry=&DrawsSheets=&UserTime=&Sanctioned={sanctioned}' \
                   r'&AgeGroup={age_group}&SearchRadius=-1&QuickSearch=6'

        table = response.xpath('//table[@id="dropdown_form"]')

        # #### 1 ####
        age_group_list = table.xpath('.//tr[1]//input/@value').getall()
        print('---------age_group_list', age_group_list)
        # ['', 'Y', 'A']
        age_group_list = age_group_list[1:]

        # #### 2 ####
        #  Get current time ,
        c = time.time()
        current_month = time.gmtime(c).tm_mon
        current_year = time.gmtime(c).tm_year

        #  Generates the values of the parameter
        year_list = [str(current_year), str(current_year + 1)]
        months_of_this_year = []
        for i in range(current_month, 12 + 1):
            months_of_this_year.append(str(i))
            i += 1
        print('----------- months_of_this_year :', months_of_this_year)
        # months_of_this_year : ['4', '5', '6', '7', '8', '9', '10', '11', '12']

        months_of_next_year = []
        for i in range(1, 12 + 1):
            months_of_next_year.append(str(i))
            i += 1
        print('----------- months_of_next_year :', months_of_next_year)
        # months_of_next_year :['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

        # #### 3 ####
        state_list = table.xpath('.//tr[5]/td[2]/select[1]/option/@value').getall()
        print('-------state : ', state_list)
        # print : ['', '', 'AA', 'AB', 'AE', 'AK', 'AL', 'AP', 'AR', 'AS', 'AZ', 'BC', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MB', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NB', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NL', 'NM', 'NS', 'NT', 'NU', 'NV', 'NY', 'OH', 'OK', 'ON', 'OR', 'PA', 'PE', 'PR', 'QC', 'RI', 'SC', 'SD', 'SK', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY', 'YT']
        state_list = state_list[2:]

        # #### 4 ####
        sanctioning_list = table.xpath('.//tr[6]/td[2]//input/@value').getall()
        print('-------sanctionings : ', sanctioning_list)
        # ['-1', '0', '39']
        sanctioning_list = sanctioning_list[1:]

        # #### 5 ####
        surfaces_list = table.xpath('.//tr[11]//select/option/@value').getall()
        print('-------surfaces : ', surfaces_list)
        #  ['', '1', '2', '5', '3', '4', '6']
        surfaces_list = surfaces_list[1:]

        # sanctioning_list = ['-1']
        # surfaces_list = ['']
        # year_list = ['2019']
        # months_of_this_year = ['4']
        state_list = ['AB']

        request_list = []
        for age_group in age_group_list:
            for year in year_list:
                for state in state_list:
                    for sanctioned in sanctioning_list:
                        for surface in surfaces_list:
                            if year == str(current_year):
                                for month in months_of_this_year:
                                    url = base_url.format(state=state, month=month, year=year, surface=surface,
                                                          sanctioned=sanctioned, age_group=age_group)
                                    # print(url)
                                    request_list.append(
                                        scrapy.Request(url=url, callback=self.parse_table, dont_filter=True))
                            else:
                                for month in months_of_next_year:
                                    url = base_url.format(state=state, month=month, year=year, surface=surface,
                                                          sanctioned=sanctioned, age_group=age_group)
                                    # print(url)
                                    request_list.append(
                                        scrapy.Request(url=url, callback=self.parse_table, dont_filter=True))
        return request_list

    def parse_table(self, response):
        self.table_count += 1
        table = response.xpath('//div[@class="TennisLinkBody"]//div[@class="CommonTable"]//table')
        if table is None:
            print('The table  is not found.............')
            return
        else:
            print('The table  is  found.............', self.table_count)

        # <a href="javascript:Go(234878);">
        #                                 L1B Sportime Schenectady Easter Classic
        #                                 -
        #                                 100059919</a>
        for link in table.xpath('.//tr/td[2]/a/@href').getall():
            # print(link, '------------------------------')

            t = re.findall('\d+', link)[0]
            url = r'https://tennislink.usta.com/Tournaments/TournamentHome/Tournament.aspx?T=' + t

            print(url)
            yield scrapy.Request(url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):

        item = TournamentItem()
        item['url'] = response.url
        response.xpath('//div[@class="tournament"]')
        item['skill_level'] = []

        for text in response.xpath('//div[@class="tournament"]/table[1]//tr[2]/td[1]/text()').getall():
            text = text.replace('\r\n', '').strip()
            if re.match('\d+', text) is not None:
                item['tournament_id'] = text

            if re.match('[a-zA-Z]+', text) is not None:
                item['skill_level'].append(text)

        item['date'] = response.xpath('//div[@class="tournament"]/table[1]//tr[2]/td[2]/text()').get(
            default='').replace('\r\n', '').strip()

        item['divisions'] = []
        for li in response.xpath('//div[@class="tournament"]/table[1]//tr[2]/td[3]/a/ul/li'):
            temp = ' '.join(li.xpath('.//text()').getall())
            temp = temp.replace('\r\n', '').strip()
            temp = re.sub(' +', ' ', temp)
            item['divisions'].append(temp)

        item['section'] = response.xpath('//div[@class="tournament"]/table[2]//tr[2]/td[1]/text()').get(
            default='')
        item['district'] = response.xpath('//div[@class="tournament"]/table[2]//tr[2]/td[2]/text()').get(
            default='')
        item['surface_type'] = response.xpath('//div[@class="tournament"]/table[2]//tr[2]/td[3]/text()').get(
            default='')
        item['draws_posted'] = response.xpath('//div[@class="tournament"]/table[2]//tr[2]/td[4]/text()').get(
            default='')
        item['last_updated'] = response.xpath('//div[@class="tournament"]/table[2]//tr[2]/td[5]/text()').get(
            default='')



        org_table = response.xpath('//table[@id="organization"]')
        item['org_name'] = org_table.xpath('.//tr[2]/td[2]/div/text()').get(default='')
        item['org_phone'] = org_table.xpath('.//tr[3]/td[2]/text()').get(default='')
        item['org_fax'] = org_table.xpath('.//tr[4]/td[2]/text()').get(default='')
        item['org_website'] = org_table.xpath('.//tr[5]/td[2]//a/text()').get(default='')



        org_address = org_table.xpath('.//tr[6]/td[2]/div/text()').getall()
        item['org_address'] = ' '.join(org_address)
        item['org_street_or_pobox'] = org_address[0]
        item['org_city'] = (org_address[1]).split(',')[0]
        item['org_state'] = re.findall('[A-Z]{2}', org_address[1])[0]
        item['org_zip_code'] = re.findall('\d+', org_address[1])[0]



        contact_table = response.xpath('//table[@id="contact"]')
        item['director'] = contact_table.xpath('.//tr[2]/td[2]/text()').get(default='')
        item['director_phone'] = contact_table.xpath('.//tr[3]/td[2]/text()').get(default='')
        item['director_cell'] = contact_table.xpath('.//tr[4]/td[2]/text()').get(default='')
        item['director_fax'] = contact_table.xpath('.//tr[5]/td[2]/text()').get(default='')
        item['director_email'] = contact_table.xpath('.//tr[6]/td[2]/text()').get(default='')
        item['referee'] = contact_table.xpath('.//tr[7]/td[2]/text()').get(default='')
        item['referee_phone'] = contact_table.xpath('.//tr[8]/td[2]/text()').get(default='')
        item['referee_email'] = contact_table.xpath('.//tr[9]/td[2]/text()').get(default='')



        entry_table = response.xpath('//table[@id="entry_info"]')
        item['entries_closed'] = entry_table.xpath('.//tr[2]/td[2]/text()').get(default='')
        item['entry_information'] = entry_table.xpath('.//tr[3]/td[2]/text()').get(default='')
        item['checks_payable_to'] = entry_table.xpath('.//tr[4]/td[2]/text()').get(default='')
        item['send_checks_to'] = entry_table.xpath('.//tr[5]/td[2]/text()').get(default='')
        item['tournament_website'] = entry_table.xpath('.//tr[6]/td[2]/text()').get(default='')



        yield item
