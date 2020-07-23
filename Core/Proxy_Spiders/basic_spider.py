# _*_coding: utf-8 _*_
# python3.6
# @Time    : 2020/07/14 下午 8:59
# @Author  : WangHe
# @Email: wangheplus@163.com
# @File    : basic_spider.py
# @Software: PyCharm

import requests
from lxml import etree

from Models import Proxy
from Utils.Set_Random_Request_Headers import get_request_headers


class BasicSpider(object):
    # 定义3个类变量：代理ip的域名列表，分组xpath->获取包含代理IP信息标签列表的xpath，详情xpath->获取代理的详情信息的xpath{'ip':'','port':'','area':''}
    urls = []
    group_xpath = ''
    detail_xpath = {}

    def __init__(self, url_list=[], g_xpath='', d_xpath={}):
        """
        初始化对象传参
        :param url_list:爬虫列表
        :param g_xpath:分组xpath
        :param detail_xpath:详情xpath
        """
        if url_list:
            self.urls = url_list
        if g_xpath:
            self.group_xpath = g_xpath
        if d_xpath:
            self.detail_xpath = d_xpath

    def get_page_from_url(self, url):
        """
        根据url发送请求，获取页面数据
        :param url:请求url
        :return:response
        """
        resp = requests.get(url=url, headers=get_request_headers())
        return resp.content

    def check_param(self, lis):
        """
        检查获取的数据是否存在，列表中有数据就返回第一个，没有就返回空字符串
        :param lis: 数据列表
        :return: 真实的数据
        """
        return lis[0].replace('\n\t', '').replace('\t', '').replace(' ', '') if len(lis) != 0 else ''

    def get_proxy_from_page(self, page):
        """
        解析页面，封装为proxy对象
        :param page:
        :return:代理对象
        """
        html = etree.HTML(page)
        tag_list = html.xpath(self.group_xpath)
        for tag in tag_list:
            proxy_ip = self.check_param(tag.xpath(self.detail_xpath['ip']))
            proxy_port = self.check_param(tag.xpath(self.detail_xpath['port']))
            proxy_area = self.check_param(tag.xpath(self.detail_xpath['area']))
            proxy = Proxy(proxy_ip=proxy_ip, proxy_port=proxy_port, proxy_area=proxy_area)
            yield proxy

    def get_proxies(self):
        for url in self.urls:
            detail = self.get_page_from_url(url)
            proxies = self.get_proxy_from_page(page=detail)
            yield from proxies


# if __name__ == '__main__':
#     param = {
#         'url_list': ['http://www.ip3366.net/free/?stype=1&page={}'.format(i) for i in range(1, 4)],
#         'g_xpath': '//*[@id="list"]/table/tbody/tr',
#         'd_xpath': {
#             'ip': './td[1]/text()',
#             'port': './td[2]/text()',
#             'area': './td[5]/text()',
#         }
#     }
#     for p in BasicSpider(**param).get_proxies():
#         print(p)
