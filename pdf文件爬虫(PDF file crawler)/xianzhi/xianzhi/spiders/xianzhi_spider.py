# -*- coding: utf-8 -*-
import scrapy
import re
from xianzhi.items import XianzhiItem

class XianzhiSpiderSpider(scrapy.Spider):
    name = 'xianzhi_spider'
    allowed_domains = ['zgganwang.org.cn']
    start_urls = ['http://www.zgganwang.org.cn/FangTan.shtml?kanwu=293']

    def parse(self, response):

        if response.status == 200:

            result_list = re.findall('tree.nodes.*"\)',response.body.decode())
            # 如下：
            # tree.nodes["c0_c45311"] = 'text:卷三十六 人物;url:javascript:treeHrefTo("45311");';

            # tree.nodes["c0_c45312"] = 'text:附录;url:javascript:treeHrefTo("45312");';

            # tree.nodes["c45276_c45313"] = 'text:第一章建置沿革;url:javascript:treeHrefTo("45313");';

            # tree.nodes["c45276_c45314"] = 'text:第二章区划治所;url:javascript:treeHrefTo("45314");';



            for i in range(len(result_list)):
                item = XianzhiItem()
                item['index'] = i

                result = result_list[i]
                # text:封面;url:javascript:treeHrefTo("45268")

                item["content"] = result

                item['title'] =  re.findall("text:.+?;",result)[0].replace("text:","").replace(";","")

                item['father'] =re.findall("tree.nodes.*]",result)[0].replace('tree.nodes["',"").replace('"]',"")

                item["kw"] = re.findall('treeHrefTo\("\d+',result)[0].replace('treeHrefTo("',"")

                item['url'] = "http://www.zgganwang.org.cn/Video.shtml?kw="+item['kw']

                yield scrapy.Request(url=item['url'], meta={'item': item}, callback=self.parse_detail,
                                     dont_filter=True)
        else:
            print("响应失败：",response.status)

    def parse_detail(self,response):
        item = response.meta["item"]

        item['pdf_url'] = []
        url = response.xpath("//iframe/@src").get()
        if url is not None:
            url = "http://www.zgganwang.org.cn"+url
        item['pdf_url'].append(url)

        yield item
