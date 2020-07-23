# _*_coding: utf-8 _*_
# python3.6
# @Time    : 2020/07/14 下午 9:10
# @Author  : WangHe
# @Email: wangheplus@163.com
# @File    : Settings.py
# @Software: PyCharm
import logging

# 1，默认最大评分，请求失败一次减一分
MAX_SCORE = 50

# 2，日志默认的配置
LOG_LEVEL = logging.DEBUG  # 默认等级
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'  # 默认日志格式
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
LOG_FILENAME = 'log.log'  # 默认日志文件名称

# 3，代理ip测试的超时时间
TEST_TIMEOUT = 10

# 4，配置mongo数据库
DB_HOST = '127.0.0.1'
DB_PORT = 27017
DB_NAME = 'WangdamaProxyPool'
DB_COLLECTION = '代理ip池'

#  5，配置爬虫路径，可扩展
PROXIES_SPIDERS = [
    'Core.Proxy_Spiders.proxy_spider.Ip3366Spider',
    'Core.Proxy_Spiders.proxy_spider.FastSpider',
    'Core.Proxy_Spiders.proxy_spider.OverseasSpider',
    'Core.Proxy_Spiders.proxy_spider.Ip66Spider',
    'Core.Proxy_Spiders.proxy_spider.BirdSpider',
    'Core.Proxy_Spiders.proxy_spider.Ip89Spider',
    'Core.Proxy_Spiders.proxy_spider.HappySpider',
]

# 6，配置爬虫运行时间间隔，单位小时
RUN_SPIDERS_INTERVAL = 6

# 7，配置检测代理IP异步任务的数量
TEST_PROXY_ASYNC_COUNT = 10

# 8，配置校验代理IP的时间间隔，单位小时
TEST_PROXY_INTERVAL = 1

# 9，配置数据库中获取的ip的最大数量，值越小，ip可用性越高，随机性越低
MAX_SELECT_PROXIES_COUNT = 10

# 自定义web服务器端口号
WEB_PORT = 15583
