# _*_coding: utf-8 _*_
# python3.6
# @Time    : 2020/07/14 下午 9:03
# @Author  : WangHe
# @Email: wangheplus@163.com
# @File    : run_spider.py
# @Software: PyCharm
import time
import schedule
import importlib

# 协程池异步开启任务，开启猴子补丁
from gevent.pool import Pool
from gevent import monkey

monkey.patch_all()

from Utils.Logs import logger
from Settings import PROXIES_SPIDERS, RUN_SPIDERS_INTERVAL
from Core.Proxy_Storages.mongo_store import MongoPool
from Core.Proxy_Validates.httpbin_validator import check_proxy


class RunSpider(object):
    def __init__(self):
        """
        实例化对象
        """
        self.mongo = MongoPool()
        self.g_pool = Pool()

    def get_spider_from_settings(self):
        """
        遍历配置的爬虫路径，获取所有爬虫入口类名
        :return:爬虫对象
        """
        for all_spider_class_name in PROXIES_SPIDERS:
            # 获取路径和类名
            path, class_name = all_spider_class_name.rsplit('.', maxsplit=1)
            # 根据路径导入模块
            module = importlib.import_module(path)
            # 从模块中根据类名获取类
            cls = getattr(module, class_name)
            # 通过类名创建爬虫对象
            spider = cls()

            yield spider

    def run(self):
        """
        遍历爬虫对象的get_proxies获取ip
        :return:
        """
        spiders = self.get_spider_from_settings()
        for spider in spiders:
            # 异步执行任务
            self.g_pool.apply_async(self.__execute_one_spider_task, args=(spider,))
        # 携程守护
        self.g_pool.join()

    def __execute_one_spider_task(self, spider):
        """
        用于处理一个爬虫任务
        :param spider: 爬虫对象
        :return:
        """
        try:
            for proxy in spider.get_proxies():
                # 校验代理ip
                validate_proxy = check_proxy(proxy)
                # 可用代理写入数据库
                if validate_proxy.proxy_speed != 0:
                    self.mongo.insert_proxy(validate_proxy)
        except Exception as e:
            logger.exception(e)

    @classmethod
    def start(cls):
        """
        第一次运行爬虫然后设置定时
        :return:
        """
        spi = RunSpider()
        spi.run()
        # 配置定时任务
        schedule.every(RUN_SPIDERS_INTERVAL).hours.do(spi.run())
        while True:
            schedule.run_pending()  # schedule检验是否到达RUN_SPIDERS_INTERVAL时间间隔
            time.sleep(30)  # 每隔30秒检查一次是否到达RUN_SPIDERS_INTERVAL的值

# if __name__ == '__main__':
#     RunSpider.start()
