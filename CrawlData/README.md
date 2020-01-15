# 后端 - 信息抓取

**Aim**

- [ ] 定时任务
- [ ] 增量爬虫 - 数据更新



**Plan**

- [ ] 首次预处理：
  - 数据库、表的创建
- [x] pipelines.py：创建管道类 -> 直接存入PostGresql数据库
- [ ] middlewares.py ：创建中间件 -> 从Redis数据库中判定，存在link过滤
- [ ] 脚本任务：
  - 预处理：从PostGresql提取数据指纹(*link*)，写入Redis数据库
  - 启动爬取任务（首先判定是否在运行）
  - 任务结束时，清空Redis数据库