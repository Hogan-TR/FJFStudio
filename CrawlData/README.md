# 后端 - 信息抓取

**Aim**

- [x] 定时任务
- [x] 增量爬虫 - 数据更新



**Plan**

- [x] 首次预处理：
  - 数据库、表的创建
- [x] pipelines.py：创建管道类 -> 直接存入PostGresql数据库
- [x] middlewares.py ：创建中间件 -> 从Redis数据库中判定，存在link过滤
- [x] 脚本任务：
  - [x] 预处理：从PostGresql提取数据指纹(*link*)，写入Redis数据库
  - [x] 启动爬取任务（首先判定是否在运行）
  - [x] 任务结束时，清空Redis数据库
  - [x] 多爬虫任务处理



**代办**

- [ ] 服务器部署

- [ ] 长期测试

**Step**

1. 创建虚拟Python环境，从Python3.5向上兼容
2. python3 ./CrawlData/dn120/dn120/db/ctable.py
3. 可先手动启动测试
4. crontab定时任务，调用script脚本(周期：一天)