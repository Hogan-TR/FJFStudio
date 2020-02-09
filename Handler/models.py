from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Text, Integer, Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import DeclarativeMeta

import json
import datetime


# 创建对象的基类
Base = declarative_base()


class Record(Base):  # 定义 Record 对象 记录
    # 表的名字
    __tablename__ = "record"

    # 表的结构
    id = Column(Integer, primary_key=True, autoincrement=True)  # 自动id
    title = Column(String(255))  # 问题
    link = Column(String(255), nullable=True)   # 原文链接
    introduction = Column(Text, nullable=True)  # 介绍
    solve = Column(ARRAY(Text), nullable=True)  # 解决方案，列表，允许为空
    img = Column(ARRAY(String), nullable=True)  # 图片列表
    add_time = Column(DateTime, default=func.now())  # 添加日期
    mod_time = Column(DateTime, default=func.now())  # 修改日期
    tags = Column(ARRAY(String), nullable=True)  # 标签列表


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values, like other classes
                    json.dumps(data)
                    fields[field] = data
                except TypeError:  # 添加了对datetime的处理
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.date):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (
                            datetime.datetime.min + data).time().isoformat()
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
