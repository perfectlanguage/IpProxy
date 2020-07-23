# _*_coding: utf-8 _*_
# python3.6
# @Time    : 2020/07/14 下午 9:09
# @Author  : WangHe
# @Email: wangheplus@163.com
# @File    : Set_Random_Request_Headers.py
# @Software: PyCharm

from fake_useragent import FakeUserAgent


def get_request_headers():
    headers = {
        'User-Agent': FakeUserAgent().random,
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
    }
    return headers
