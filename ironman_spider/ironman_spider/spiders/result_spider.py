# -*- coding: utf-8 -*-
import scrapy
import json
from ironman_spider.settings import AGEGROUP, COUNTRY, SEX
from ironman_spider.items import ResultItem


class ResultSpider(scrapy.Spider):
    name = 'result_spider'
    allowed_domains = ['ironman.com']

    def __init__(self, race=None, y=None, *args, **kwargs):
        super(ResultSpider, self).__init__(*args, **kwargs)
        print(race, y)
        self.race = race
        self.y = y
        self.racename_url_list = json.load(open("race_name.json", "r", encoding="utf-8"))

        # http://eu.ironman.com/triathlon/events/americas/ironman-70.3/st.-george/results.aspx
        # join: ?p=1&race=stgeorge70.3&rd=20180505&y=2018&sex=F&agegroup=18-24&loc=#axzz5shkzUaho

    def start_requests(self):
        res = []
        base_url = ''
        for racename_url in self.racename_url_list:
            if self.race == racename_url['name']:
                base_url = racename_url['url']

        for agegroup in AGEGROUP:
            for sex in SEX:
                for i in range(1, 30 + 1):
                    url = base_url + "?p={p}&race={race}&y={y}&sex={sex}&agegroup={agegroup}&loc=#axzz5shkzUaho".format(
                        p=i, race=self.race, y=self.y, sex=sex, agegroup=agegroup)
                    gender = sex
                    category = agegroup
                    print(url)
                    res.append(
                        scrapy.Request(url, meta={"gender": gender, "category": category}, callback=self.parse_item,
                                       dont_filter=True))
        return res

    def parse_item(self, response):

        table = response.xpath('//table[@id="eventResults"]')

        if table is None:
            return

        tr_list = table.xpath('./tbody/tr')

        if tr_list is None:
            return

        gender = response.meta["gender"]
        category = response.meta["category"]

        for tr in tr_list:
            item = ResultItem()
            item["gender"] = gender
            item["category"] = category

            item["name"] = tr.xpath('./td/a/text()').get()
            item["country"] = tr.xpath('./td[2]/text()').get()

            item["div_rank"] = tr.xpath('./td[3]/text()').get()
            item["gender_rank"] = tr.xpath('./td[4]/text()').get()
            item["overall_rank"] = tr.xpath('./td[5]/text()').get()
            item["swim_time"] = tr.xpath('./td[6]/text()').get()
            item["bike_time"] = tr.xpath('./td[7]/text()').get()
            item["run_time"] = tr.xpath('./td[8]/text()').get()

            yield item
