from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Text, Integer, Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

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
