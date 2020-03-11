# coding=utf-8
import redis
import random
# from adslproxy.config import *
import pymysql


class RedisClient(object):
    def __init__(self, host, port, password):
        """
        初始化Redis连接
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis 密码
        :param proxy_key: Redis 哈希表名
        """
        proxy_key = 'adsl'
        pool = redis.ConnectionPool(host=host, port=port, password=password, decode_responses=True)
        self.db = redis.StrictRedis(connection_pool=pool)
        self.proxy_key = proxy_key

    def set(self, name, proxy):
        """
        设置代理
        :param name: 主机名称
        :param proxy: 代理
        :return: 设置结果
        """
        return self.db.hset(self.proxy_key, name, proxy)

    def get(self, name):
        """
        获取代理
        :param name: 主机名称
        :return: 代理
        """
        return self.db.hget(self.proxy_key, name)

    def count(self):
        """
        获取代理总数
        :return: 代理总数
        """
        return self.db.hlen(self.proxy_key)

    def remove(self, name):
        """
        删除代理
        :param name: 主机名称
        :return: 删除结果
        """
        return self.db.hdel(self.proxy_key, name)

    def names(self):
        """
        获取主机名称列表
        :return: 获取主机名称列表
        """
        return self.db.hkeys(self.proxy_key)

    def proxies(self):
        """
        获取代理列表
        :return: 代理列表
        """
        return self.db.hvals(self.proxy_key)

    def random(self):
        """
        随机获取代理
        :return:
        """
        proxies = self.proxies()
        return random.choice(proxies)

    def all(self):
        """
        获取字典
        :return:
        """
        return self.db.hgetall(self.proxy_key)


    def hash_get(self, name, k):
        res = self.db.hget(name, k)

        return res



    def hash_set(self, name, k, v):
        self.db.hset(name, k, v)


    def hash_getall(self, name):
        res = self.db.hgetall(name)
        self.db.rpush()

        return res


    def hash_del(self, name, k):
        res = self.db.hdel(name, k)
        if res:
            print('Deleted successfully. ')
            return 1
        else:
            print('Delete failed.The key does not exist ')
            return 0

    @property  # 属性方法，
    # 使用的时候和变量一个用法就好比实例，A=MyRedis(), A.clean_redis使用，
    # 如果不加这个@property,使用时A=MyRedis(), A.clean_redis()   后面需要加这个函数的括号
    def clean_redis(self):
        self.db.flushdb()  # 清空 redis
        print('清空redis成功！')
        return 0


class MySQLClient():
    def __init__(self, host, user, passwd, dbName):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbName = dbName
        self.connection = pymysql.connect(self.host, self.user, self.passwd, self.dbName, charset="utf8")
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def get_one(self, sql):
        res = None
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except:
            print("查询mysql数据库失败....")
        return res

    def get_all(self, sql):
        res = ()
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except Exception as e:

            print("查询失败", e)
        # return res

    def insert(self, sql):
        return self.__edit(sql)

    def update(self, sql):
        return self.__edit(sql)

    def delete(self, sql):
        return self.__edit(sql)

    def __edit(self, sql):
        # count = 0
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            self.close()
        except Exception as e:
            print("事务提交失败", e)
            self.connection.rollback()
        # return count
