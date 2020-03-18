# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class CalbarSpiderItem(scrapy.Item):
class LawyerItem(scrapy.Item):
    detail_url = scrapy.Field()
    name = scrapy.Field()
    license_status = scrapy.Field()
    number = scrapy.Field()
    city = scrapy.Field()
    admission_date = scrapy.Field()





    address = scrapy.Field()
    county = scrapy.Field()
    phone_number = scrapy.Field()
    fax_number = scrapy.Field()
    email = scrapy.Field()
    law_school = scrapy.Field()
    cla_sections = scrapy.Field()
    certified_legal_specialty = scrapy.Field()








