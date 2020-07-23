# _*_coding: utf-8 _*_
# python3.6
# @Time    : 2020/07/14 下午 9:04
# @Author  : WangHe
# @Email: wangheplus@163.com
# @File    : Proxy_Api.py
# @Software: PyCharm
import json
from flask import Flask, request

from Core.Proxy_Storages.mongo_store import MongoPool
from Settings import MAX_SELECT_PROXIES_COUNT,WEB_PORT


class ProxyApi(object):
    def __init__(self):
        self.mongo = MongoPool()

        self.app = Flask(__name__)

        @self.app.route('/random/one')
        def random():
            """
            根据protocol和domain提供一个高可用代理ip，通过protocol和domain参数对ip过滤
            :return:
            """
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxy = self.mongo.get_random_one_proxy(protocol, domain, count=MAX_SELECT_PROXIES_COUNT)
            if protocol:
                return '{}://{}:{}'.format(protocol, proxy.proxy_ip, proxy.proxy_port)
            else:
                return '{}:{}'.format(proxy.proxy_ip, proxy.proxy_port)

        @self.app.route('/match/more')
        def proxies():
            """
            根据protocol和domain提供多个高可用代理ip，通过protocol和domain参数对ip过滤，给指定ip追加不可用域名
            :return:
            """
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')

            # proxy_lis是Proxy对象列表，无法直接json序列化，需要转换成字典列表再序列化
            proxy_obj_lis = self.mongo.get_proxy_list(protocol, domain,
                                                      count=MAX_SELECT_PROXIES_COUNT)
            proxy_lis = [p.__dict__ for p in proxy_obj_lis]
            # TODO json.dumps格式化输出：ensure_ascii=False 解决中文乱码 ， indent=4 格式化输出树状结构，然并卵
            return json.dumps(proxy_lis, ensure_ascii=False, indent=4)

        @self.app.route('/not/domain')
        def disable_domain():
            """
            在获取ip的时候指定了不可用域名参数，将不再获取这个ip，提高ip可用性
            :return:
            """
            ip = request.args.get('ip')
            domain = request.args.get('domain')
            if ip is None:
                return '请提供ip参数'
            if domain is None:
                return '请提供域名domain参数'
            else:
                self.mongo.post_disable_domain(ip=ip, domain=domain)
                return '{}禁用域名{}成功'.format(ip, domain)

    def run(self):
        """
        flask开启web服务接口
        :return:
        """
        self.app.run('0.0.0.0', port=WEB_PORT)

    @classmethod
    def start(cls):
        """
        统一的web服务开启接口
        :return:
        """
        proxy_api = cls()
        proxy_api.run()


# if __name__ == '__main__':
#     ProxyApi.start()
