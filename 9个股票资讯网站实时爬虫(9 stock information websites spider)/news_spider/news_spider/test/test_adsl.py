# -*- coding: utf-8 -*-
from adslproxy import RedisClient

import time
client = RedisClient(host='47.107.227.145', port=6379, password='diF_76_daU($#dKi)*7&1285#@', proxy_key='adsl')

while True:
    time.sleep(1)
    try:
        random = client.random()
        all = client.all()
        names = client.names()
        proxies = client.proxies()
        count = client.count()
        #
        print('RANDOM:', random)
        print('ALL:', all)
        print('NAMES:', names)
        print('PROXIES:', proxies)
        print('COUNT:', count)

    except Exception as e:
        print(e)
