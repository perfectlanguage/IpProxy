# _*_coding: utf-8 _*_
# python3.6
# @Time    : 2020/07/14 下午 9:03
# @Author  : WangHe
# @Email: wangheplus@163.com
# @File    : Proxy_Test.py
# @Software: PyCharm

import time
import schedule

from gevent.pool import Pool
from queue import Queue
from gevent import monkey

monkey.patch_all()

from Core.Proxy_Storages.mongo_store import MongoPool
from Core.Proxy_Validates.httpbin_validator import check_proxy
from Settings import MAX_SCORE, TEST_PROXY_ASYNC_COUNT, TEST_PROXY_INTERVAL


class ProxyTest(object):
    def __init__(self):
        """
        实例化数据库，队列，协程池
        """
        self.mongo = MongoPool()
        self.queue = Queue()
        self.g_pool = Pool()

    def __check_callback(self, temp):
        """
        循环开启异步回调
        :param temp: 占位参数
        :return:
        """
        self.g_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)

    def run(self):
        proxies = self.mongo.find_all_proxy()
        for proxy_ in proxies:
            # 代理ip添加到队列中
            self.queue.put(proxy_)

        for i in range(TEST_PROXY_ASYNC_COUNT):
            # 异步开启任务
            self.g_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)
        # 队列守护
        self.queue.join()

    def __check_one_proxy(self):
        """
        从队列中获取ip进行校验，并更新到数据库
        :return:
        """
        # 1，从队列中获取数据，调用check_proxy()方法校验
        _proxy = self.queue.get()
        proxy = check_proxy(_proxy)

        # 2，代理不可用，分数减1
        if proxy.proxy_speed == 0:
            proxy.proxy_score -= 1
            # 2.1，分数为0，数据库中删除代理数据
            if proxy.proxy_score == 0:
                self.mongo.delete_proxy(proxy)
            # 2.2，否则更新代理数据
            else:
                self.mongo.update_proxy(proxy)

        # 3，代理可用，回复分值，更更新到数据库
        else:
            proxy.proxy_score = MAX_SCORE
            self.mongo.update_proxy(proxy)

        # 4，调用队列的task_done()方法表示当前任务完成
        self.queue.task_done()

    @classmethod
    def start(cls):
        """
        开启定时任务
        :return:
        """
        pt = cls()
        pt.run()
        schedule.every(TEST_PROXY_INTERVAL).hours.do(pt.run)
        while True:
            schedule.run_pending()
            time.sleep(30)


# if __name__ == '__main__':
#     ProxyTest.start()
