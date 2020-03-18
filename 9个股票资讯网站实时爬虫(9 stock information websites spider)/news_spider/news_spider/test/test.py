# -*- coding: utf-8 -*-
import time
import datetime
import re
# a = "2019年05月16日 18:26:27"
# d = datetime.datetime.strptime(a, "%Y年%m月%d日 %H:%M:%S")
# t = d.timetuple()
# timeStamp = int(time.mktime(t))
#
# print(timeStamp)


# temp = '2019年05月16日         18:26:27'
# print('<<<<<<<<<<< ' + temp + ' >>>>>>>>>>>')
#
# d = datetime.datetime.strptime(temp, "%Y年%m月%d日 %H:%M:%S")
# t = d.timetuple()
# timeStamp = int(time.mktime(t))
#
# temp ='''
#                【压垮乐视网的最后一根稻草竟然是它！】15日，进入暂停上市状态第三天的乐视网披露，因乐视体育经营不利导致增资协议中的对赌条款失败，乐视体育股东之一的前海思拓提出的涉及回购融资股权的仲裁申请，得到了北京仲裁委员会的支持。
#                '''
#
# print()


# for i in range(1,10+1):
#     print('https://developers.whatismybrowser.com/useragents/explore/software_name/uc-browser/{}'.format(str(i)))


# date = '2019-05-17T03:12:25Z'
#
# date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
#
# date = date + datetime.timedelta(hours =8)
# print(date)


# print(int(time.time()))
try:
    # raise Exception('X')
    i = [1,2]
    print(i[3])
except Exception as e:
    print(str(e))
    print("{0}".format(str(e)))


