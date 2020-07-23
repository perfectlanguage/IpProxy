# _*_coding: utf-8 _*_
# python3.6
# @Time    : 2020/07/14 下午 8:57
# @Author  : WangHe
# @Email: wangheplus@163.com
# @File    : mongo_store.py
# @Software: PyCharm

import pymongo
import random

from Utils.Logs import logger
from Settings import DB_HOST, DB_PORT, DB_NAME, DB_COLLECTION
from Models import Proxy


class MongoPool(object):
    def __init__(self):
        """
        建立数据库连接
        """
        self.collection = pymongo.MongoClient(host=DB_HOST, port=DB_PORT)
        dbs = self.collection[DB_NAME]
        self.proxies = dbs[DB_COLLECTION]

    def __del__(self):
        """
        关闭数据库连接
        """
        self.collection.close()

    def insert_proxy(self, proxy):
        """
        写入数据到数据库
        :param proxy: 代理ip对象
        :return:
        """
        if self.proxies.count({'_id': proxy.proxy_ip}) == 0:
            proxy_dic = proxy.__dict__
            proxy_dic['_id'] = proxy.proxy_ip  # 将代理的ip作为主键(_id)
            self.proxies.insert_one(proxy_dic)
            logger.info('存储新的代理：{}'.format(proxy))
        else:
            logger.warning('已经存在的代理：{}'.format(proxy))

    def update_proxy(self, proxy):
        """
        修改数据库数据
        :param proxy: 代理ip对象
        :return:
        """
        self.proxies.update_one({'_id': proxy.proxy_ip}, {'$set': proxy.__dict__})
        logger.info('更新成功的代理：{}'.format(proxy))

    def delete_proxy(self, proxy):
        """
            删除数据库数据
            :param proxy: 代理ip对象
            :return:
        """
        self.proxies.delete_one({'_id': proxy.proxy_ip})
        logger.info('删除的代理：{}'.format(proxy))

    def find_all_proxy(self):
        """
        查询所有的数据库数据
        :return: 代理ip(proxy对象)
        """
        cursor = self.proxies.find()
        for item in cursor:
            item.pop('_id')  # 删除数据库的主键
            proxy = Proxy(**item)
            yield proxy

    def find(self, query_dict={}, count=0):
        """
        实现查询的功能：根据条件进行查询，可以指定查询的数量，先分数降序，再速度升序，保证优质的代理
        :param query_dict: 查询条件字典
        :param count: 查询数据个数
        :return: 满足查询条件的ip(proxy对象)列表
        """
        cursor = self.proxies.find(query_dict, limit=count).sort(
            [('proxy_score', pymongo.DESCENDING), ('proxy_speed', pymongo.ASCENDING)])
        proxy_list = []
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    def get_proxy_list(self, protocol=None, disable_domain=None, nick_type=1, count=0):
        """
        实现根据协议类型和要访问的域名获取指定数量的代理ip列表
        :param protocol:协议类型， http=1,https=2,http/https=3
        :param disable_domain:代理支持的域名，jd.con或者taobao.com等
        :param nick_type:匿名类型，默认高匿，高匿=1,匿名=2,透明=3
        :param count:限制获取代理的个数，默认获取所有的
        :return:满足要求的代理ip列表
        """
        # 1，匿名
        query_dic = {'proxy_nick_type': nick_type}

        # 2，域名
        if disable_domain:
            query_dic['proxy_disable_domains'] = {'$nin': [disable_domain, ]}

        # 3，协议
        if protocol is None:
            # 返回既支持http又支持https的代理
            query_dic['proxy_protocol'] = 3
        elif protocol.lower() == 'http':
            # 返回支持http的代理
            query_dic['proxy_protocol'] = {'$in': [1, 3]}
        else:
            # 返回支持https的代理
            query_dic['proxy_protocol'] = {'$in': [2, 3]}

        return self.find(query_dict=query_dic, count=count)

    def get_random_one_proxy(self, protocol=None, disable_domain=None, nick_type=1, count=0):
        """
        根据协议类型和要访问的域名获取一个随机的代理ip
        :param protocol:协议类型， http=1,https=2,http/https=3
        :param disable_domain:代理支持的域名，jd.con或者taobao.com等
        :param nick_type:匿名类型，默认高匿，高匿=1,匿名=2,透明=3
        :param count:
        :return:满足要求的一个随机代理ip
        """
        proxy_list = self.get_proxy_list(protocol=protocol, disable_domain=disable_domain,
                                         nick_type=nick_type, count=count)
        return random.choice(proxy_list)

    def post_disable_domain(self, ip, domain):
        """
        实现将指定的域名添加到指定ip的proxy_disable_domains列表中
        :param ip:ip地址
        :param domain:域名
        :return:
        """
        if self.proxies.count({'_id': ip}, {'proxy_disable_domains': domain}) == 0:
            # 该域名不存在就添加
            self.proxies.update_one({'_id': ip}, {'$push': {'proxy_disable_domains': domain}})
            logger.info('代理{}添加不可用域名{}成功'.format(ip, domain))
        logger.warning('代理{}中已经存在不可用域名{}'.format(ip, domain))
