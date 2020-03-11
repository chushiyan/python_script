# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class TencentspiderItem(scrapy.Item):

    # 职位名，Job title
    positionName = scrapy.Field()

    # 详情连接， url of the job's detail
    positionLink = scrapy.Field()

    # 职位类别，job category
    positionType = scrapy.Field()

    # 工作职责，
    jobDuties = scrapy.Field()

    # 工作要求，
    jobRequirement = scrapy.Field()

    # 招聘人数，Number of Hiring
    peopleNumber = scrapy.Field()

    # 工作地点，the Work Location
    workLocation = scrapy.Field()

    # 发布时间，teh job posting time
    publishTime = scrapy.Field()
