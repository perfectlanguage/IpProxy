# _*_coding: utf-8 _*_
# python3.6
# @Time    : 2020/07/14 下午 9:01
# @Author  : WangHe
# @Email: wangheplus@163.com
# @File    : Proxy_Spiders.py
# @Software: PyCharm

import time
import random
import requests

from Core.Proxy_Spiders.basic_spider import BasicSpider
from Utils.Set_Random_Request_Headers import get_request_headers


class Ip3366Spider(BasicSpider):
    """
    1,云代理
    """
    urls = ['http://www.ip3366.net/free/?stype={}&page={}'.format(s, p) for s in range(1, 4, 2) for p in range(1, 8)]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }


class FastSpider(BasicSpider):
    """
    2,快代理
    """
    urls = ['https://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, 11)]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }

    def get_page_from_url(self, url):
        # 反爬策略，设置随机等待时间(1到3秒)
        time.sleep(random.uniform(1, 3))
        # 调用父类方法,发送请求获取响应
        return super().get_page_from_url(url)


class OverseasSpider(BasicSpider):
    """
    3,国外代理
    """
    urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}'.format(i) for i in range(1, 7)]
    group_xpath = '//*[@id="page"]/table[2]/tr[position()>2]'
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[5]/text()',
    }


class Ip66Spider(BasicSpider):
    """
    4,66代理
    """
    urls = ['http://www.66ip.cn/{}.html'.format(i) for i in range(1, 11)]
    group_xpath = '//div[contains(@class,"containerbox ")]/div[1]/table/tr[position()>1]'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()',
    }


class BirdSpider(BasicSpider):
    """
    5,蝶鸟代理
    """
    urls = ['https://www.dieniao.com/FreeProxy/{}.html'.format(i) for i in range(1, 7)]
    group_xpath = '//div[contains(@class,"free-main")]/ul/li[position()>1]'
    detail_xpath = {
        'ip': './span[1]/text()',
        'port': './span[2]/text()',
        'area': './span[4]/text()'
    }


class Ip89Spider(BasicSpider):
    """
    6,89代理
    """
    urls = ['http://www.89ip.cn/index_{}.html'.format(i) for i in range(1, 11)]
    group_xpath = '//table[@class="layui-table"]/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()'
    }

    def get_page_from_url(self, url):
        # 重写父类方法，修改返回值的格式，防止中文乱码
        resp = requests.get(url=url, headers=get_request_headers())
        return resp.text


class HappySpider(BasicSpider):
    """
    7,开心代理
    """
    urls = ['http://www.kxdaili.com/dailiip/{}/{}.html'.format(i, j) for i in range(1, 3) for j in range(1, 11)]
    group_xpath = '//table[@class="active"]/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[6]/text()'
    }


# if __name__ == '__main__':
#     spider = HappySpider()
#     l = []
#     for proxy in spider.get_proxies():
#         l.append(proxy)
#         print(type(proxy), proxy)
#     print(len(l))
