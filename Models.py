# _*_coding: utf-8 _*_
# python3.6
# @Time    : 2020/07/14 下午 9:08
# @Author  : WangHe
# @Email: wangheplus@163.com
# @File    : Models.py
# @Software: PyCharm


from Settings import MAX_SCORE


class Proxy(object):

    def __init__(self, proxy_ip, proxy_port, proxy_protocol=0, proxy_nick_type=0, proxy_speed=0, proxy_area=None,
                 proxy_score=MAX_SCORE, proxy_disable_domains=[]):
        """协议类型(http=1,https=2,http/https=3)和匿名程度(高匿=1,匿名=2,透明=3)和ip响应速度(单位秒)为0表示ip不可用"""

        # 代理的ip
        self.proxy_ip = proxy_ip
        # 代理的端口号
        self.proxy_port = proxy_port
        # 代理支持的协议类型    http=1,https=2,http/https=3
        self.proxy_protocol = proxy_protocol
        # 代理的匿名程度   高匿=1,匿名=2,透明=3
        self.proxy_nick_type = proxy_nick_type
        # 代理的响应速度  单位秒
        self.proxy_speed = proxy_speed
        # 代理所在的区域
        self.proxy_area = proxy_area
        # 代理的评分，默认最大值，请求失败一次扣一分，直到减为0
        self.proxy_score = proxy_score
        # 代理的不可用域名列表  有的代理在某些域名下不可用，在别的域名可用
        self.proxy_disable_domains = proxy_disable_domains

    def __str__(self):
        # 数据以字符串的形式输出
        return str(self.__dict__)
