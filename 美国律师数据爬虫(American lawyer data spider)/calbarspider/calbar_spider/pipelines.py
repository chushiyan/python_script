# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import csv


class JsonPipeline(object):
    def __init__(self):
        self.file = open("result_.json", "a", encoding='utf-8')
        # the json file start with a '['
        self.file.write('[')

    def process_item(self, item, spider):
        json_line = json.dumps(dict(item)) + ",\n"
        self.file.write(json_line)

    def close_spider(self, spider):
        #  let the json file end with a ']'
        self.file.write(']')
        self.file.close()


class CSVPipeline(object):

    def __init__(self):

        self.file = open('result.csv', 'wb')
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        # detail_url = scrapy.Field()
        # name = scrapy.Field()
        # license_status = scrapy.Field()
        # number = scrapy.Field()
        # city = scrapy.Field()
        # admission_date = scrapy.Field()
        #
        # address = scrapy.Field()
        # county = scrapy.Field()
        # phone_number = scrapy.Field()
        # fax_number = scrapy.Field()
        # email = scrapy.Field()
        # law_school = scrapy.Field()
        # cla_sections = scrapy.Field()
        # certified_legal_specialty = scrapy.Field()
        name = item['name'] if (item['name'] is not None) else 'null'
        license_status = item['license_status'] if (item['license_status'] is not None) else 'null'
        number = item['number'] if (item['number'] is not None) else 'null'
        city = item['city'] if (item['city'] is not None) else 'null'
        admission_date = item['admission_date'] if (item['admission_date'] is not None) else 'null'
        address = item['address'] if (item['address'] is not None) else 'null'
        county = item['county'] if (item['county'] is not None) else 'null'
        phone_number = item['phone_number'] if (item['phone_number'] is not None) else 'null'
        fax_number = item['fax_number'] if (item['fax_number'] is not None) else 'null'
        email = item['email'] if (item['email'] is not None) else 'null'
        law_school = item['law_school'] if (item['law_school'] is not None) else 'null'
        cla_sections = item['email'] if (item['email'] is not None) else 'null'
        email = item['email'] if (item['email'] is not None) else 'null'

        if item['image_name']:
            self.writer.writerow((item['image_name'].encode('utf8', 'ignore'), item['image_urls']))
        return item


    def close_spider(self, spider):

        self.file.close()