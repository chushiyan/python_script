# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


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
        self.file = open("result.csv", 'w', encoding='utf-8', newline="")
        self.writer = csv.writer(self.file, delimiter=',', quotechar='"')
        self.writer.writerow(
            [
                # 'url',
                '城市',
                '区域',
                '街/路',
                '小区名称',
                '房屋总数',
                '物业公司',
                '开发商'
            ]
        )

    def process_item(self, item, spider):
        self.writer.writerow(
            [
                # item['community_url'],
                item['city'],
                item['district'],
                item['load'],
                item['community'],
                item['house_totol'],
                item['property_companies'],
                item['developer']
            ])
        return item

    def closed_spider(self, spider):
        self.file.close()

