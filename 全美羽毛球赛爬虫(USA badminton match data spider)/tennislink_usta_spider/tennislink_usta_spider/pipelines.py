# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json


# ############## 1 ################
class NotFoundPipeline(object):
    def process_item(self, item, spider):
        for key, value in item.items():
            if value == "":
                item[key] = 'not-found'

            # if type(value) == list and len(value) == 0:
            #     item[key] = 'not-found'
        return item


# ############## 2 ################
class NoSpacePipeline(object):
    def process_item(self, item, spider):
        for key, value in item.items():
            if key == 'org_address':
                value = value.replace('&nbsp', '').replace('Map', '').replace('\u00a0', ' ').strip()

            if type(value) == str:
                value = value.replace('\r\n', '').replace('\n', '').replace('\r', '').strip()

            if type(value) == list and len(value) > 0:
                for i in range(len(value)):
                    value[i] = value[i].replace('\r\n', '').replace('\n', '').replace('\r', '').strip()

            item[key] = value
        return item



# ############## 4 ################
class CSVPipeline(object):

    def __init__(self):
        self.file = open("result.csv", 'w', encoding='utf-8', newline="")
        self.writer = csv.writer(self.file, delimiter=',', quotechar='"')
        first_row = (
            'tournament_id',
            'skill_level',
            'date',
            'divisions',
            'section',
            'district',
            'surface_type',
            'draws_posted',
            'last_updated',
            'org_name',
            'org_phone',
            'org_fax',
            'org_website',
            'org_address',
            'org_street_or_pobox',
            'org_city',
            'org_state',
            'org_zip_code',
            'director',
            'director_phone',
            'director_cell',
            'director_fax',
            'director_email',
            'referee',
            'referee_phone',
            'referee_email',
            'entries_closed',
            'entry_information',
            'checks_payable_to',
            'send_checks_to',
            'tournament_website'
        )
        self.writer.writerow(first_row)

    def process_item(self, item, spider):
        row = (
            item['tournament_id'],
            ' '.join(item['skill_level']),
            item['date'],
            ' '.join(item['divisions']),
            item['section'],
            item['district'],
            item['surface_type'],
            item['draws_posted'],
            item['last_updated'],
            item['org_name'],
            item['org_phone'],
            item['org_fax'],
            item['org_website'],
            item['org_address'],
            item['org_street_or_pobox'],
            item['org_city'],
            item['org_state'],
            item['org_zip_code'],

            item['director'],
            item['director_phone'],
            item['director_cell'],
            item['director_fax'],
            item['director_email'],
            item['referee'],
            item['referee_phone'],
            item['referee_email'],
            item['entries_closed'],
            item['entry_information'],
            item['checks_payable_to'],
            item['send_checks_to'],
            item['tournament_website'],
        )
        self.writer.writerow(row)
        return item

    def closed_spider(self, spider):
        self.file.close()


# ############## 5 ################
class JSONPipeline(object):

    def __init__(self):
        self.file = open("result_.json", 'w', encoding='utf-8')
        self.file.write('[')
        self.file.write('\n')

    def process_item(self, item, spider):
        json_line = json.dumps(dict(item)) + ",\n"
        self.file.write(json_line)
        return item

    def close_spider(self, spider):
        #  let the json file end with a ']'
        self.file.write(']')
        self.file.close()
