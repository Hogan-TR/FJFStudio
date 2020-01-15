# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Dn120Item(scrapy.Item):
    id = scrapy.Field()  # 唯一标志
    title = scrapy.Field()  # 标题
    link = scrapy.Field()  # 原文链接
    tags = scrapy.Field()  # 标签
    content = scrapy.Field()  # 介绍 + 内容
    img_list = scrapy.Field()  # 图片列表
