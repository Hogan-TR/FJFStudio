# -*- coding: utf-8 -*-

# Pre-Process - DataBase
# Connect to DataBase and Creat Table


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, TIMESTAMP, Text, Integer, Table, ForeignKey, create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, sessionmaker

from scrapy.utils.project import get_project_settings

# 创建对象的基类
Base = declarative_base()

# 从 settings.py 获取配置
settings = get_project_settings()


class Record(Base):  # 定义 Record 对象 记录
    # 表的名字
    __tablename__ = "record"

    # 表的结构
    id = Column(Integer, primary_key=True, autoincrement=True)  # 唯一标识
    title = Column(String(255))  # 问题
    link = Column(String(255))   # 原文链接 - 作为"数据指纹"
    introduction = Column(Text, nullable=True)  # 介绍
    solve = Column(ARRAY(Text), nullable=True)  # 解决方案，列表，允许为空
    img = Column(ARRAY(String), nullable=True)  # 图片列表
    add_time = Column(DateTime, default=func.now())  # 添加日期
    mod_time = Column(DateTime, default=func.now())  # 修改日期
    tags = Column(ARRAY(String), nullable=True)  # 标签列表


# 初始化数据库连接
engine = create_engine(settings.get('PG_STR'),
                       encoding='utf-8', echo=False, pool_size=100, pool_recycle=10)

# 创建 DBSession 类型
DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)  # 创建表
