import os
import time
import datetime
from scrapy import cmdline
# from scrapy.utils.project import get_project_settings
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dn120.models import Record


minute = 0  # 统计分钟
checkFile = "isRunning.txt"  # 运行标记文件名
startTime = datetime.datetime.now()  # 脚本运行时间
# Settings = get_project_settings()  # 从 scrapy 的配置文件获取


class DataTransfer(object):  # 预处理类
    def __init__(self):
        # 创建Redis连接
        # self.redisdb = redis.StrictRedis(host=Settings.get('REDIS_HOST'), port=Settings.get(
        #     'REDIS_PORT'), password=Settings.get('REDIS_PASSWORD'), decode_responses=True)
        self.redisdb = redis.StrictRedis(
            host='127.0.0.1', port='6379', password=None, decode_responses=True)

        # 创建Postgresql连接
        engine = create_engine(
            "postgresql+psycopg2://postgres:320683@localhost:5432/test", encoding='utf-8')
        DBSession = sessionmaker(bind=engine)
        self.pgsession = DBSession()

        # Redis 的 set-key
        # self.set_key = Settings.get('REDIS_SET_KEY')
        self.set_key = 'fingerprint'

    def load_data(self):  # 加载所用link
        return self.pgsession.query(Record.link).all()

    def add_data(self, data):  # 向Redis添加记录
        """
            Returns:
                - 0 已存在
                - 1 成功加入
        """
        return self.redisdb.sadd(self.set_key, data)

    def handler(self):
        res = self.load_data()
        for each in res:  # 逐条加入
            self.add_data(each[0])

    def clean(self):
        self.redisdb.delete(self.set_key)  # 清空set

    def close(self):
        self.pgsession.close()  # 断开连接


while True:
    isRunning = os.path.isfile(checkFile)
    if not isRunning:  # 爬虫不在运行, 开始启动
        clawerTime = datetime.datetime.now()
        waitTime = clawerTime - startTime
        print(
            f"At time:{clawerTime}, start clawer, waitTime:{waitTime}")

        conn = DataTransfer()  # 实例化
        conn.handler()  # 数据迁移
        conn.close()  # 预处理完成，断开连接

        # cmdline.execute('scrapy crawl xitongcheng'.split())
        os.system("scrapy crawl xitongcheng")  # 受限于学生机性能 - 单次仅执行一个
        time.sleep(120)  # 暂停2分钟
        os.system("scrapy crawl jb51")

        conn.clean()  # 清空 set(可省略)
        endTime = datetime.datetime.now()
        print(f"At time:{endTime}, end clawer, spendTime: {endTime-clawerTime}")
        break  # 爬虫结束后，退出脚本
    else:
        print(
            f"At time:{datetime.datetime.now()}, Scrapy is running, sleep to wait.")
    time.sleep(600)  # 每10分钟检查一次
    minute += 10
    if minute >= 86400:  # 一天 24h, 86400min
        break
