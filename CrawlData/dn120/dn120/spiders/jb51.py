# -*- coding: utf-8 -*-
import scrapy
from dn120.items import Dn120Item


class Jb51Spider(scrapy.Spider):
    name = 'jb51'
    allowed_domains = ['jb51.net']
    start_urls = ['https://www.jb51.net/os/']

    # 取大类
    def parse(self, response):
        base_url = 'https://www.jb51.net'
        ca = response.xpath('//h2//text() | //h2//@href').extract()
        for i in range(0, len(ca), 2):
            url = base_url + ca[i]
            Request = scrapy.Request(url, callback=self.parse_pages)
            Request.meta['data'] = {
                'keyword': ca[i+1].split('/'),
                'url': url
            }
            yield Request

    def parse_pages(self, response):
        base_url = 'https://www.jb51.net'
        details_url = response.xpath(
            '//li/div[@class="item-inner"]//@href').extract()
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

    def parse_items(self, response):
        isAll = response.xpath('//a[text()="阅读全文"]/@href').extract_first()

        if isAll:  # 阅读全文
            Request = scrapy.Request(
                response.meta['data']['url']+isAll, callback=self.parse_items)
            Request.meta['data'] = response.meta['data']
            yield Request
        else:
            item = Dn120Item()
            item['content'] = dict()

            # 标签
            tags = response.meta['data']['keyword']
            if isinstance(tags, list):
                item['tags'] = tags
            else:
                item['tags'] = [tags]

            # 链接
            item['link'] = response.url

            # 标题
            item['title'] = response.xpath(
                '//h1[@class="title"]/text()').extract_first()

            # 图片列表 有防盗链 无效
            item['img_list'] = response.xpath('//p/img/@src').extract()

            # 介绍
            introduction = response.xpath(
                '//div[@class="summary"]/text()').extract_first()

            # 解决方案
            solve = list()
            temp = response.xpath('//div[@id="content"]/p[not(@style)]/text() | //div[@id="content"]/p[not(@style)]//strong/text() | //div[@id="content"]/p[not(@style)]//a/text() | //code').extract()
            for x in temp:
                if x.strip() != '':
                    solve.append(x.strip())

            item['content']['introduction'] = introduction
            item['content']['solve'] = solve

            yield item
