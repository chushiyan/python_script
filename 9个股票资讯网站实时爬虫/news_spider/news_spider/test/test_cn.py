# -*- coding: utf-8 -*-
import requests


for i in range(1,10+1):
    response = requests.get('http://irm.cninfo.com.cn/')
    response.encoding ='utf-8'
    with open('cn{}.html'.format(str(i)),'w',encoding='utf-8') as f:
        f.write(response.text)



