# -*- coding: utf-8 -*-
import scrapy
from alibaba.items import ProviderItem
import urllib.parse


class ProviderSpider(scrapy.Spider):
    name = 'provider'
    allowed_domains = ['1688.com']

    # start_urls = [
    #     'https://s.1688.com/company/company_search.htm?keywords=USB%B7%E7%C9%C8&button_click=top&earseDirect=false&n=y&netType=1%2C11&_source=sug']

    def start_requests(self):
        reqs = []
        # base_url = 'https://s.1688.com/company/company_search.htm?keywords={}&button_click=top&earseDirect=false&n=y&netType=1%2C11&_source=sug'
        base_url = 'https://s.1688.com/company/company_search.htm?keywords={}'

        keys = [
            # "USB风扇",
            "USB迷你小风扇",
            "手握风扇",
            "无叶风扇",
            "加湿器",
            "空气净化器",
            "皂液机",
            "车载冰箱",
            "LED化妆镜",
            "LED手电筒",
            "手持工具",
            "车载吸尘器",
            "手持吸尘器",
            "净水器",
            "血糖仪",
            "户外马桶",
            "灭蝇灯",
            "灭蚊灯",
            "美容仪",
            "吹飞机",
            "吸尘器",
            "电子产品",
            "化妆镜",
            "血糖仪",
            "血压仪",
            "按摩椅",
            "检测仪",
            "电动工具",
            "电饭锅",
            "蓝牙音箱",
            "机箱",
            "鼠标",
            "键盘",
            "数码礼品",
            "农耕机",
            "塑业有限公司",
            "精密模具有限公司",
            "电器有限公司",
            "科技有限公司",
            "用品有限公司",
            "医疗制品有限公司",
            "医疗机械有限公司",
            "医疗有限公司",
            "包装有限公司",
            "厨卫有限公司",
            "电器科技有限公司",
            "健康科技有限公司",
            "电器有限公司",
            "灯具有限公司",
            "户外用品有限公司"
        ]

        # keys = [
        #     "USB风扇",
        # ]

        for key in keys:
            # 注意：阿里巴巴页面使用的是gbk
            key = urllib.parse.quote(key, encoding='gbk')
            url = base_url.format(key)
            # print('########################################', key)
            print('#######################', url, '#######################')
            req = scrapy.Request(url=url, callback=self.parse_page, dont_filter=True)

            reqs.append(req)
        return reqs

    def parse_page(self, response):

        lis = response.xpath('//div[@id="sw_mod_mainblock"]/div/ul/li')

        if lis is None:
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%% 未找到结果列表 %%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%% 下面代码不执行 %%%%%%%%%%%%%%%%%%%%%%%%%%%')
            return

        for li in lis:
            item = ProviderItem()
            # 1、提取公司网址
            item['url'] = li.xpath('.//div[@class="list-item-title"]/a/@href').get()

            # 2、提取公司名称
            item['company_name'] = li.xpath('.//div[@class="list-item-title"]/a/text()').get()

            # 3、提取主营产品
            item['main_product'] = li.xpath('.//div[@class="detail-left"]/div[1]/a/span/text()').getall()

            # 4、提取经营模式
            item['business_model'] = li.xpath('.//div[@class="detail-right"]//div[1]/b/text()').get()

            temp_list = []
            for div in li.xpath('.//div[@class="list-item-detail"]/div/div'):
                # temp = ''
                desc = div.xpath('./span/text()').get()

                # 有些所在地显示不全，以...省略，但是a链接的title是全的，so
                info = div.xpath('./a/@title').get()
                # 但是其他信息的a链接没有title，所以通过text()获取文本
                if info is None:
                    info = div.xpath('./a/text()').get()

                if (desc is not None) and (info is not None):
                    temp = desc + info
                    temp_list.append(temp)

            # print('------------------------------------------')
            # print(temp_list)
            # print('------------------------------------------')

            # 为什么不直接通过xpath获取，因为有些没有厂房面积等信息，
            # 代之以  累计成交数: --   累计买家数: --  重复采购率: --
            for temp in temp_list:

                # 5、提取所在地
                if '所在地' in temp:
                    item['location'] = temp.split(':')[1]

                # 6、提取员工人数
                if '员工人数' in temp:
                    item['number_of_employees'] = temp.split(':')[1]

                # 7、提取工艺类型
                if '工艺类型' in temp:
                    item['process_types'] = temp.split(':')[1]

                # 8、提取加工方式
                if '加工方式' in temp:
                    item['process_method'] = temp.split(':')[1]

                # 9、提取厂房面积
                if '厂房面积' in temp:
                    item['factory_area'] = temp.split(':')[1]

            # print('------------------------------------------')
            # print(item)
            # print('------------------------------------------')

            yield item

        link_list = response.xpath('//div[@class="page-bottom"]/a/text()').getall()
        print('########################################')
        if link_list is None:
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%% 未找到分页按钮 %%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%% 下面代码不执行 %%%%%%%%%%%%%%%%%%%%%%%%%%%')
            return
        print(link_list)
        print('########################################')

        if "下一页" == link_list[-1]:
            next_url = response.xpath('//div[@class="page-bottom"]/a[last()]/@href').get()
            yield scrapy.Request(url=next_url, callback=self.parse_page, dont_filter=True)
