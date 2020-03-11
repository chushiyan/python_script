# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tencentSpider.items import TencentspiderItem


class TencentspiderSpider(CrawlSpider):
    name = 'TencentSpider'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0#a']

    rules = (

        # LinkExtractor(allow=r'position\.php\?&start=\d*#a')
        # Response里链接的提取规则，返回的符合匹配规则的链接匹配对象的列表

        # extract the Pagination Buttons' urls.They look like the following urls:
        # position.php?&start=10#a
        # position.php?&start=20#a

        # 定义规则，抓取符合要求的url
        # allow是允许爬取的规则，后面的内容是正则表达式，匹配页面中所有符合匹配规则的a标签
        # callback是回调函数，用于解析抓取到的符合匹配的链接
        # follow：是否跟进，是否继续请求抓取到的链接
        Rule(LinkExtractor(allow=r'position\.php\?&start=\d*#a'), callback='parse_item', follow=True),

        # 编写匹配详情页的规则，抓取到详情页的链接后不用跟进
        # position_detail.php?id=40658&keywords=&tid=0&lid=0
        Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d*&keywords=&tid=0&lid=0'), callback='parse_detail',
             follow=False),
    )

    def parse_item(self, response):

        table = response.xpath('//table[@class="tablelist"]')

        if not table:
            self.logger.error("###### The table which warps the jobs' list is not found. ######")

        for tr in table.xpath('.//tr[@class="even"] | .//tr[@class="odd"]'):
            item = TencentspiderItem()
            item['positionName'] = tr.xpath('./td[1]/a/text()').get()
            item['positionLink'] = 'https://hr.tencent.com/' + tr.xpath('./td[1]/a/@href').get()
            item['positionType'] = tr.xpath('./td[2]/text()').get()
            item['peopleNumber'] = tr.xpath('./td[3]/text()').get()
            item['workLocation'] = tr.xpath('./td[4]/text()').get()
            item['publishTime'] = tr.xpath('./td[5]/text()').get()

            yield item

    def parse_detail(self, response):

        item = TencentspiderItem()

        # There are two uls whose class equals "squareli"' in the job's detail page.
        uls = response.xpath('//ul[@class="squareli"]')

        # extract all li's text in the ul
        # method getall() return a list
        # notice：It will raise a exception if use string() to get all text.
        item['jobDuties'] = uls[0].xpath('.//text()').getall()
        item['jobRequirement'] = uls[1].xpath('.//text()').getall()

        yield item
