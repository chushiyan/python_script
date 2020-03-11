# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


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


class NoSpacePipeline(object):
    def process_item(self, item, spider):
        for key, value in item.items():
            if type(value) == str:
                value = value.replace('\r\n', '').replace('\n', '').replace('\r', '').replace('\t', '').strip()

            if type(value) == list and len(value) > 0:
                for i in range(len(value)):
                    value[i] = value[i].replace('\r\n', '').replace('\n', '').replace('\r', '').replace('\t', '').strip()

            item[key] = value
        return item
