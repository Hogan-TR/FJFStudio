# -*- coding: utf-8 -*-
import scrapy
from dn120.items import Dn120Item


class XitongchengSpider(scrapy.Spider):
    name = 'xitongcheng'
    allowed_domains = ['xitongcheng.com']
    start_urls = ['http://www.xitongcheng.com/jiaocheng/']

    # 取大类
    def parse(self, response):
        more = response.xpath(
            '//div[@class="jc_type"]//h2//text() | //div[@class="jc_type"]//div[@class="more"]/a/@href').extract()
        base_url = 'http://www.xitongcheng.com/jiaocheng/'
        for i in range(0, len(more), 2):
            url = base_url + more[i + 1]
            Request = scrapy.Request(url, callback=self.parse_pages)
            Request.meta['data'] = {
                "keyword": more[i].replace("教程", ""), "url": url}
            yield Request
            # Ex of data: {'keyword': 'Xp系统', 'url': 'http://www.xitongcheng.com/jiaocheng/xp/'}

        # Request = scrapy.Request(
        #     'http://www.xitongcheng.com/jiaocheng/xp/', callback=self.parse_pages)
        # Request.meta['data'] = {'keyword': 'Xp系统',
        #                         'url': 'http://www.xitongcheng.com/jiaocheng/xp/'}
        # yield Request

    # 取详情界面URL
    def parse_pages(self, response):
        base_url = "http://www.xitongcheng.com"
        details_url = response.xpath(
            '//ul[not(@*)]//a[@target="_blank"]/@href').extract()
        next_page = response.xpath('//a[text()="下一页"]/@href').extract_first()

        for url in details_url:
            url = base_url + url
            Request = scrapy.Request(url, callback=self.parse_items)
            Request.meta['data'] = response.meta['data']
            yield Request

        if next_page:
            next_page = response.meta['data']['url'] + next_page
            Request = scrapy.Request(next_page, callback=self.parse_pages)
            Request.meta['data'] = response.meta['data']
            yield Request

    # 详情界面解析
    def parse_items(self, response):
        item = Dn120Item()
        item['content'] = dict()

        tags = response.meta['data']['keyword']
        if isinstance(tags, list):
            item['tags'] = tags
        else:
            item['tags'] = [tags]

        item['link'] = response.url
        item['title'] = response.xpath('//h1/text()').extract_first()

        img_list = response.xpath('//p/img/@src').extract()
        item['img_list'] = img_list

        introduction = ''
        temp = response.xpath('//div[@class="content"]/p[1]//text()').extract()
        for x in temp:
            introduction += x.strip()
        item['content']['introduction'] = introduction

        solve = []
        temp = response.xpath(
            '//div[@class="content"]/p[position()>1]//text()').extract()
        for x in temp:
            if x.strip() != '':
                solve.append(x.strip())
        item['content']['solve'] = solve

        yield item
