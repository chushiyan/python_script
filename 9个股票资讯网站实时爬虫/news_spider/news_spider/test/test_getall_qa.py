# -*- coding: utf-8 -*-
from adslproxy import RedisClient
import json
import time
client = RedisClient(host='47.107.227.145',
                     port=6379,
                     password='diF_76_daU($#dKi)*7&1285#@',
                     proxy_key='QAItem')

try:
    # random = client.random()
    all = client.all()
    with open('QAItem.json','w',encoding='utf-8') as f:
        f.write(json.dumps(all,ensure_ascii=False))
    # print(all)
except Exception as e:
    print(e)
