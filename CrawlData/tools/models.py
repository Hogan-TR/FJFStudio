from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Text, Integer, Table, ForeignKey, create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, sessionmaker


# 创建对象的基类
Base = declarative_base()

# record_m2m_tag = Table("record_m2m_tag", Base.metadata,
#                        Column("id", Integer, primary_key=True),
#                        Column("record_id", Integer, ForeignKey("record.id")),
#                        Column("tag_id", Integer, ForeignKey("tag.id"))
#                        )


# class Tag(Base):  # 定义 Tag 对象 标签
#     __tablename__ = "tag"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(255))
#     add_time = Column(DateTime, default=func.now())


class Record(Base):  # 定义 Record 对象 记录
    # 表的名字
    __tablename__ = "record"

    # 表的结构
    id = Column(Integer, primary_key=True, autoincrement=True)  # 唯一标识，参考哈希
    title = Column(String(255))  # 问题
    link = Column(String(255), nullable=True)   # 原文链接
    introduction = Column(Text, nullable=True)  # 介绍
    solve = Column(ARRAY(Text), nullable=True)  # 解决方案，列表，允许为空
    img = Column(ARRAY(String), nullable=True)  # 图片列表
    add_time = Column(DateTime, default=func.now())  # 添加日期
    mod_time = Column(DateTime, default=func.now())  # 修改日期
    tags = Column(ARRAY(String), nullable=True)  # 标签列表
    # tags = relationship("Tag", secondary=record_m2m_tag, backref="record")


# # 初始化数据库连接
engine = create_engine('postgresql+psycopg2://postgres:#bb991119#@localhost:6116/test',
                       encoding='utf-8', echo=False, pool_size=100, pool_recycle=10)

# # 创建 DBSession 类型
DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    # 创建DBSession类型:
    Base.metadata.create_all(engine)  # 创建表
