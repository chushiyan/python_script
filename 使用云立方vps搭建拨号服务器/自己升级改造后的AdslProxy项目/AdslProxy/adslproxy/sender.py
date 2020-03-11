# coding=utf-8
import re
import time
import requests
from requests.exceptions import ConnectionError, ReadTimeout
from adslproxy.db import RedisClient
from adslproxy.config import *
import platform

import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler


if platform.python_version().startswith('2.'):
    import commands as subprocess
elif platform.python_version().startswith('3.'):
    import subprocess
else:
    raise ValueError('python version must be 2 or 3')


class Sender():

    def __init__(self):

        self.redis = RedisClient()

        # 日志打印格式
        log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
        formatter = logging.Formatter(log_fmt)
        # 创建TimedRotatingFileHandler对象
        self.log_file_handler = TimedRotatingFileHandler(filename="adsl.log", when="D", interval=1, backupCount=7)

        self.log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
        self.log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
        self.log_file_handler.setFormatter(formatter)
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger()
        self.log.addHandler(self.log_file_handler)


    def __del__(self):
        self.remove_proxy()

    def get_ip(self, ifname=ADSL_IFNAME):
        """
        获取本机IP
        :param ifname: 网卡名称
        :return:
        """
        (status, output) = subprocess.getstatusoutput('ifconfig')
        if status == 0:
            pattern = re.compile(ifname + '.*?inet.*?(\d+\.\d+\.\d+\.\d+).*?netmask', re.S)
            result = re.search(pattern, output)
            if result:
                ip = result.group(1)
                return ip

    def test_proxy(self, proxy):
        """
        测试代理
        :param proxy: 代理
        :return: 测试结果
        """
        try:
            response = requests.get(TEST_URL, proxies={
                'http': 'http://' + proxy,
                #'https': 'https://' + proxy
            }, timeout=TEST_TIMEOUT)
            if response.status_code == 200:
                return True
        except (ConnectionError, ReadTimeout):
            return False

    def remove_proxy(self):
        """
        移除代理
        :return: None
        """
        # TODO
        # self.redis = RedisClient()
        self.redis.remove(CLIENT_NAME)
        self.log.info("Successfully Removed Proxy")
        self.log.addHandler(self.log_file_handler)

    def set_proxy(self, proxy):
        """
        设置代理
        :param proxy: 代理
        :return: None
        """
        # TODO
        # self.redis = RedisClient()
        if self.redis.set(CLIENT_NAME, proxy):
            self.log.info("Successfully Set Proxy : %s"%proxy)
            self.log.addHandler(self.log_file_handler)

    def adsl(self):
        """
        拨号主进程
        :return: None
        """
        while True:
            self.log.info("ADSL is Starting, And Removing Proxy, Please wait......")
            self.log.addHandler(self.log_file_handler)
            try:
                self.remove_proxy()
                self.redis = None
            except:
                while True:
                    (status, output) = subprocess.getstatusoutput(ADSL_BASH)
                    if status == 0:
                        self.redis = RedisClient()
                        self.remove_proxy()
                        self.redis = None
                        break

            self.redis = None
            (status, output) = subprocess.getstatusoutput(ADSL_BASH)
            self.redis = RedisClient()
            if status == 0:

                self.log.info("ADSL Successfully")
                self.log.addHandler(self.log_file_handler)

                ip = self.get_ip()

                if ip:
                    self.log.info("The new IP is : %s"%ip)
                    self.log.info("Testing Proxy, Please Wait")
                    self.log.addHandler(self.log_file_handler)

                    proxy = '{ip}:{port}'.format(ip=ip, port=PROXY_PORT)
                    if self.test_proxy(proxy):

                        self.log.info("This is a valid proxy")
                        self.set_proxy(proxy)

                        self.log.info('The program is sleeping for %s second'%ADSL_CYCLE)
                        self.log.addHandler(self.log_file_handler)

                        time.sleep(ADSL_CYCLE)
                    else:
                        self.log.warning("Oops.This is a invalid proxy")
                        self.log.addHandler(self.log_file_handler)
                else:
                    self.log.warning("Get IP Failed, Re Dialing")
                    self.log.addHandler(self.log_file_handler)
                    time.sleep(ADSL_ERROR_CYCLE)
            else:
                self.log.warning("Oops.ADSL Failed, Please Check")
                self.log.addHandler(self.log_file_handler)
                time.sleep(ADSL_ERROR_CYCLE)


def run():

    sender = Sender()
    sender.adsl()


if __name__ == '__main__':
    run()
