# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Record


# class Dn120Pipeline(object): # Json文件存储
# def __init__(self):
#     self.file = open('dan120.json', 'wb')
#     self.exporter = JsonItemExporter(
#         self.file, encoding='utf-8', ensure_ascii=False)
#     self.exporter.start_exporting()

# def close_spider(self, spider):
#     self.exporter.finish_exporting()
#     self.file.close()

# def process_item(self, item, spider):
#     self.exporter.export_item(item)
#     return item


class Dn120Pipeline(object):  # Postgresql 数据库存储
    def __init__(self, PG_STR):
        self.PG_STR = PG_STR

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            PG_STR=crawler.settings.get('PG_STR'),
        )

    def open_spider(self, spider):  # 建立数据库连接
        engine = create_engine(self.PG_STR, encoding='utf-8')
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def process_item(self, item, spider):  # 必须
        data = Record(title=item['title'], link=item['link'], tags=item['tags'],
                      introduction=item['content']['introduction'], solve=item['content']['solve'], img=item['img_list'])
        self.session.add(data)
        self.session.commit()
        return item

    def close_spider(self, spider):  # 关闭数据库连接
        self.session.close()
