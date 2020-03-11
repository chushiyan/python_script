# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import csv


class CSVPipeline(object):

    def __init__(self):
        self.file = open("result.csv", 'w', encoding='utf-8',newline="")
        self.writer = csv.writer(self.file, delimiter=',', quotechar='"')
        self.writer.writerow([
            'Pub_Title',
            'Year',
            'Pub_Outlet',
            'Citaton_Count',
            'Abstract',
            'Author1',
            'Author1 Insttute',
            'Author2',
            'Author2 Insttute',
            'Author3',
            'Author3 Insttute',
            'Author4',
            'Author4 Insttute',
            'Author5',
            'Author5 Insttute',
            'Author6',
            'Author6 Insttute',
            'Author7',
            'Author7 Insttute',
            'Author8',
            'Author8 Insttute',
            'Author9',
            'Author9 Insttute',
            'Author10',
            'Author10 Insttute',
            'Author11',
            'Author11 Insttute',
            'Author12',
            'Author12 Insttute',
            'Tag1',
            'Tag2',
            'Tag3',
            'Tag4',
            'Tag5',
            'Tag6',
            'Tag7',
            'Tag8',
            'Tag9',
            'Tag10',
            'Tag11',
            'Tag12',
            'Tag13',
            'Tag14',
            'Tag15',
            'Tag16']
        )

    def process_item(self, item, spider):

        Author1 = "not-found"
        Author1_Insttute = "not-found"
        Author2 = "not-found"
        Author2_Insttute = "not-found"
        Author3 = "not-found"
        Author3_Insttute = "not-found"
        Author4 = "not-found"
        Author4_Insttute = "not-found"
        Author5 = "not-found"
        Author5_Insttute = "not-found"
        Author6 = "not-found"
        Author6_Insttute = "not-found"
        Author7 = "not-found"
        Author7_Insttute = "not-found"
        Author8 = "not-found"
        Author8_Insttute = "not-found"
        Author9 = "not-found"
        Author9_Insttute = "not-found"
        Author10 = "not-found"
        Author10_Insttute = "not-found"
        Author11 = "not-found"
        Author11_Insttute = "not-found"
        Author12 = "not-found"
        Author12_Insttute = "not-found"
        Tag1 = "not-found"
        Tag2 = "not-found"
        Tag3 = "not-found"
        Tag4 = "not-found"
        Tag5 = "not-found"
        Tag6 = "not-found"
        Tag7 = "not-found"
        Tag8 = "not-found"
        Tag9 = "not-found"
        Tag10 = "not-found"
        Tag11 = "not-found"
        Tag12 = "not-found"
        Tag13 = "not-found"
        Tag14 = "not-found"
        Tag15 = "not-found"
        Tag16 = "not-found"

        try:
            Author1 = item['Author'][0][0]
            Author1_Insttute = item['Author'][0][1]
            Author2 = item['Author'][1][0]
            Author2_Insttute = item['Author'][1][1]
            Author3 = item['Author'][2][0]
            Author3_Insttute = item['Author'][2][1]
            Author4 = item['Author'][3][0]
            Author4_Insttute = item['Author'][3][1]
            Author5 = item['Author'][4][0]
            Author5_Insttute = item['Author'][4][1]
            Author6 = item['Author'][5][0]
            Author6_Insttute = item['Author'][5][1]
            Author7 = item['Author'][6][0]
            Author7_Insttute = item['Author'][6][1]
            Author8 = item['Author'][7][0]
            Author8_Insttute = item['Author'][7][1]
            Author9 = item['Author'][8][0]
            Author9_Insttute = item['Author'][8][1]
            Author10 = item['Author'][9][0]
            Author10_Insttute = item['Author'][9][1]
            Author11 = item['Author'][10][0]
            Author11_Insttute = item['Author'][10][1]
            Author12 = item['Author'][11][0]
            Author12_Insttute = item['Author'][11][1]
        except Exception as e:
            print(e)

        try:
            Tag1 = item['Tag'][0]
            Tag2 = item['Tag'][1]
            Tag3 = item['Tag'][2]
            Tag4 = item['Tag'][3]
            Tag5 = item['Tag'][4]
            Tag6 = item['Tag'][5]
            Tag7 = item['Tag'][6]
            Tag8 = item['Tag'][7]
            Tag9 = item['Tag'][8]
            Tag10 = item['Tag'][9]
            Tag11 = item['Tag'][10]
            Tag12 = item['Tag'][11]
            Tag13 = item['Tag'][12]
            Tag14 = item['Tag'][13]
            Tag15 = item['Tag'][14]
            Tag16 = item['Tag'][15]
        except Exception as e:
            print(e)

        self.writer.writerow([
            item['Pub_Title'],
            item['Year'],
            item['Pub_Outlet'],
            item['Citation_Count'],
            item['Abstract'],
            Author1,
            Author1_Insttute,
            Author2,
            Author2_Insttute,
            Author3,
            Author3_Insttute,
            Author4,
            Author4_Insttute,
            Author5,
            Author5_Insttute,
            Author6,
            Author6_Insttute,
            Author7,
            Author7_Insttute,
            Author8,
            Author8_Insttute,
            Author9,
            Author9_Insttute,
            Author10,
            Author10_Insttute,
            Author11,
            Author11_Insttute,
            Author12,
            Author12_Insttute,
            Tag1,
            Tag2,
            Tag3,
            Tag4,
            Tag5,
            Tag6,
            Tag7,
            Tag8,
            Tag9,
            Tag10,
            Tag11,
            Tag12,
            Tag13,
            Tag14,
            Tag15,
            Tag16]
        )

        return item

    def closed_spider(self, spider):
        self.file.close()


class JSONPipeline(object):

    def __init__(self):
        self.file = open("result.json", 'w', encoding='utf-8')
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


class NoSpacePipeline(object):
    def process_item(self, item, spider):
        for key, value in item.items():
            if key == "Author":
                continue

            if type(value) == str:
                value = value.strip()

            if type(value) == list and len(value) > 0:
                for i in range(len(value)):
                    value[i] = value[i].strip()

            item[key] = value
        return item
