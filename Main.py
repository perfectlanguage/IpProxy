# _*_coding: utf-8 _*_
# python3.6
# @Time    : 2020/07/14 下午 9:10
# @Author  : WangHe
# @Email: wangheplus@163.com
# @File    : Main.py
# @Software: PyCharm

from multiprocessing import Process

# 爬虫，校验，api接口
from Core.Proxy_Spiders.run_spider import RunSpider
from Core.Proxy_Test import ProxyTest
from Core.Proxy_Api import ProxyApi


def run():
    """
    爬虫，校验，API模块统一接口，多进程
    :return:
    """
    process_list = []

    # 进程列表添加任务
    process_list.append(Process(target=RunSpider.start))
    process_list.append(Process(target=ProxyTest.start))
    process_list.append(Process(target=ProxyApi.start))

    for process in process_list:
        process.daemon = True  # 主进程守护
        process.start()  # 进程开启

    for p in process_list:
        p.join()  # 等待子进程完成


if __name__ == '__main__':
    run()
