# -*- coding: utf-8 -*-

0
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
import hashlib
import pymysql
from . import db
import pickle
from scrapy.exceptions import DropItem
import pymysql


class NoSpacePipeline(object):
    def process_item(self, item, spider):
        for key, value in item.items():
            if type(value) == str:
                value = value.strip()
                item[key] = value
        return item


class TimePipeline(object):
    def process_item(self, item, spider):
        item['timestamp'] = time.time()
        return item

class RedisPipeline(object):
    def __init__(self):
        # TODO 需要切换redis
        # self.client = db.RedisClient(host='47.107.227.145', password='diF_76_daU($#dKi)*7&1285#@', port=6379)
        self.client = db.RedisClient(host='localhost', port=6379, password='diF_76_daU($#dKi)*7&1285#@')

    def close_spider(self, spider):
        self.client = None

    def process_item(self, item, spider):
        if item.flag == 1:
            myid = hashlib.md5((item.get('title', '') + item.get('content', '')).encode(encoding='UTF-8')).hexdigest()
            if self.client.hash_get(item['source'], myid) is None:
                item_json = {
                    "source": item['source'],
                    "pubDate": item.get('pubDate', ''),
                    "timestamp": item['timestamp'],
                    'title': item.get('title', ''),
                    'content': item.get('content', '')
                }
                self.client.hash_set(item['source'], myid, json.dumps(item_json, ensure_ascii=False))
            else:
                raise DropItem

        if item.flag == 2:
            myid = hashlib.md5((item.get('question', '') + item.get('answer', '')).encode(encoding='UTF-8')).hexdigest()
            item_json = {
                "source": item['source'],
                "pubDate": item.get('pubDate', ''),
                "timestamp": item['timestamp'],
                'question': item.get('question', ''),
                'answer': item.get('answer', ''),
                'stockcode': item.get('stockcode', ''),
            }
            if self.client.hash_get(item['source'], myid) is None:
                self.client.hash_set(item['source'], myid, json.dumps(item_json, ensure_ascii=False))
            else:
                raise DropItem

        if item.flag == 3:
            myid = hashlib.md5((item.get('code', '') + item.get('timestamp', '')).encode(encoding='UTF-8')).hexdigest()
            if self.client.hash_get('ErrorItem', myid) is None:
                item_json = {
                    "code": item.get('code', ''),
                    "url": item.get('url', ''),
                    'timestamp': item.get('timestamp', ''),
                    'site': item.get('site', ''),
                    'desc': item.get('desc', ''),
                    'exception': item.get('exception', ''),
                }
                self.client.hash_set('ErrorItem', myid, json.dumps(item_json, ensure_ascii=False))
            else:
                raise DropItem




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
