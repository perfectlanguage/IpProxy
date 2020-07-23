# _*_coding: utf-8 _*_
# python3.6
# @Time    : 2020/07/14 下午 8:58
# @Author  : WangHe
# @Email: wangheplus@163.com
# @File    : httpbin_validator.py
# @Software: PyCharm

import time
import json
import requests

from Settings import TEST_TIMEOUT
from Utils.Logs import logger
from Utils.Set_Random_Request_Headers import get_request_headers
from Models import Proxy


def check(proxies_, is_http=True):
    # 默认值代理类型（高匿=1,匿名=2,透明=3）和响应速度（单位秒）
    proxy_nick_type = None
    proxy_speed = 0

    # 1，判断http/https
    if is_http:
        target_url = 'http://httpbin.org/get'
    else:
        target_url = 'https://httpbin.org/get'
    try:
        # 2，判断响应速度
        start_time = time.time()
        resp = requests.get(url=target_url, headers=get_request_headers(), proxies=proxies_, timeout=TEST_TIMEOUT)
        if resp.ok:
            proxy_speed = round(time.time() - start_time, 2)  # 保留两位小数

            # 3，判断匿名程度
            origin_dic = json.loads(resp.text)
            origin = origin_dic['origin']
            pc = origin_dic['headers'].get('Proxy-Connection', None)
            if ',' in origin:
                proxy_nick_type = 3  # 透明代理
            elif pc:
                proxy_nick_type = 2  # 匿名代理
            else:
                proxy_nick_type = 1  # 高匿代理

            return True, proxy_nick_type, proxy_speed
        return False, proxy_nick_type, proxy_speed
    except Exception as e:
        # logger.exception(e)
        return False, proxy_nick_type, proxy_speed


def check_proxy(proxy):
    proxies = {
        'http': 'http://{}:{}'.format(proxy.proxy_ip, proxy.proxy_port),
        'https': 'https://{}:{}'.format(proxy.proxy_ip, proxy.proxy_port)
    }
    http, http_nick_type, http_speed = check(proxies)
    https, https_nick_type, https_speed = check(proxies, False)
    if http and https:
        proxy.proxy_protocol = 3
        proxy.proxy_nick_type = https_nick_type
        proxy.proxy_speed = https_speed
    elif https:
        proxy.proxy_protocol = 2
        proxy.proxy_nick_type = https_nick_type
        proxy.proxy_speed = https_speed
    elif http:
        proxy.proxy_protocol = 1
        proxy.proxy_nick_type = http_nick_type
        proxy.proxy_speed = http_speed
    else:
        proxy.proxy_protocol = 0
        proxy.proxy_nick_type = 0
        proxy.proxy_speed = 0

    return proxy


# if __name__ == '__main__':
#     pro = Proxy('47.103.25.160', port='8118')
#     print(check_proxy(pro))

