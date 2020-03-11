# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CountdownSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class NoSpacePipeline(object):
    def process_item(self, item, spider):
        for key, value in item.items():
            if type(value) == str:
                value = value.replace('\r\n', '').replace('\n', '').replace('\r', '').replace('\t', '').strip()
                item[key] = value
        return item


import json


class JSONPipeline(object):
    def __init__(self):
        self.file = open("result.json", 'w', encoding='utf-8')
        self.file.write('[')
        self.file.write('\n')

    def process_item(self, item, spider):
        json_line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(json_line)
        return item

    def close_spider(self, spider):
        #  let the json file end with a ']'
        self.file.write(']')
        self.file.close()


import csv

class CSVPipeline(object):
    def __init__(self):
        self.file = open("result.csv", "w", encoding="utf-8",newline="")
        self.writer = csv.writer(self.file, delimiter=',', quotechar='"')
        self.writer.writerow(["date",
                              "title",
                              "url",
                              "price",
                              "volumeSize",
                              "unitOfMeasurement"])

    def process_item(self, item, spider):
        self.writer.writerow([item.get("date", "null"),
                              item.get("title", "null"),
                              item.get("url", "null"),
                              item.get("price", "null"),
                              item.get("volumeSize", "null"),
                              item.get("unitOfMeasurement", "null")])
        return item

    def close_spider(self, spider):
        self.file.close()
