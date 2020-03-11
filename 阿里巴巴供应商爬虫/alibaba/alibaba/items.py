# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProviderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    url = scrapy.Field()

    company_name = scrapy.Field()

    main_product = scrapy.Field()

    business_model = scrapy.Field()

    location =scrapy.Field()

    process_types = scrapy.Field()

    number_of_employees = scrapy.Field()

    process_method = scrapy.Field()

    factory_area = scrapy.Field()
    #
    # linkman = scrapy.Field()
    #
    # telephone = scrapy.Field()
    #
    fax = scrapy.Field()
    #
    # mobile_phone = scrapy.Field()

class ProviderContactItem(scrapy.Item):
    url = scrapy.Field()
    linkman = scrapy.Field()
    linkman_position = scrapy.Field()
    telephone = scrapy.Field()
    fax = scrapy.Field()
    mobile_phone = scrapy.Field()




