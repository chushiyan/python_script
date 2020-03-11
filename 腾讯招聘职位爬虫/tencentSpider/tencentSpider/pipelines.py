# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TencentspiderPipeline(object):
    def __init__(self):
        self.file = open("tencent_jobs.json", "a", encoding='utf-8')
        # the json file start with a '['
        self.file.write('[')

    def process_item(self, item, spider):

        # json_line = json.dumps(dict(item)) + ",\n"
        # 里面有汉字，输出的会是该汉字的ascii 字符码，而不是真正的中文。
        # 这是因为json.dumps 序列化时对中文默认使用的ascii编码.
        # 想输出真正的中文需要指定ensure_ascii=False：
        json_line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(json_line)

    def close_spider(self, spider):
        #  let the json file end with a ']'
        self.file.write(']')
        self.file.close()
