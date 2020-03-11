# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class JSONPipeline(object):

    def __init__(self):
        self.racename_file = open("res.json", 'w', encoding='utf-8')
        self.racename_file.write('[')
        self.racename_file.write('\n')

    def process_item(self, item, spider):
        json_line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.racename_file.write(json_line)
        return item

    def close_spider(self, spider):
        #  let the json file end with a ']'
        self.racename_file.write(']')
        self.racename_file.close()


from openpyxl import Workbook

class XLSXPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        title = ["Name",
                 "Country",
                 "Gender",
                 "Category",
                 "Div rank",
                 "Gender rank",
                 "Overall rank",
                 "Swim time",
                 "Bike time",
                 "Run time"]
        self.ws.append(title)

    def process_item(self, item, spider):

        line = [item["name"],
                item["country"],
                item["gender"],
                item["category"],
                item["div_rank"],
                item["gender_rank"],
                item["overall_rank"],
                item["swim_time"],
                item["bike_time"],
                item["run_time"]]

        self.ws.append(line)
        # return item

    def close_spider(self, spider):
        self.wb.save(spider.race + "-" + spider.y + '.xlsx')
