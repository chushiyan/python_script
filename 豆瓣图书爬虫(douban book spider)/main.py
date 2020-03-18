import requests
import random
from lxml import etree
import time, re
import sqlite3

connection = sqlite3.connect('douban_book.db')
cursor = connection.cursor()

cursor.execute('drop table if exists book')
cursor.execute('''
        create table book(
           book_url             varchar(256) primary key,
           title                varchar(256),
           author               varchar(256),
           publisher            varchar(256),
           img_url              varchar(256),
           comment1             varchar(1024),
           comment2             varchar(1024),
           comment3             varchar(1024),
           comment4             varchar(1024),
           comment5             varchar(1024))
    ''')

sql = ''' insert into book
              (book_url,title,author,publisher,img_url,comment1,comment2, comment3,comment4,comment5)
              values
              (:book_url,:title,:author,:publisher,:img_url,:comment1,:comment2,:comment3,:comment4,:comment5)'''

url_list = [
    "https://book.douban.com/top250?start=0",
    "https://book.douban.com/top250?start=25",
    "https://book.douban.com/top250?start=50",
    "https://book.douban.com/top250?start=75",
    # "https://book.douban.com/top250?start=100"
]

ua_list = [
    "Mozilla/5.0 (Linux; U; Android 4.4.4; en-US; SM-J110G Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.2.8.945 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; Micromax A102 Build/MicromaxA102) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.1.5.890 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; PPC)/UC Browser7.8.0.95",
    "Nokia200/2.0 (11.81) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; nokia200) U2/1.0.0 UCBrowser/8.9.0.251 U2/1.0.0 Mobile",
    "Mozilla/5.0 (iPad; U; CPU OS 5_1 like Mac OS X) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10 UCBrowser/2.2.2.259",
    "NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 OPENWAVE/UC Browser7.8.0.95/70/351 UNTRUSTED/1.0",
    "Nokia302/5.0 (14.53) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; nokia302) UCBrowser8.3.1.161/69/355/UCWEB Mobile",
    "Nokia200/2.0 (11.81) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; nokia200) AppleWebKit/530.13 (KHTML, like Gecko) UCBrowser/8.5.0.185/82/405/UCWEB Mobile UNTRUSTED/1.0",
    "Mozilla/5.0 (Linux; U; Android 6.0; zh-CN; EVA-AL10 Build/HUAWEIEVA-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.2.5.884 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-CN; HTC 919d Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.9.10.788 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J210F Build/MMB29Q) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; ASUS_Z010D Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.0.828 U3/0.8.0 Mobile Safari/534.30",
    "UCWEB/2.0 (Java; U; MIDP-2.0; en-US; SpreadTrum6530) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile UNTRUSTED/1.0",
    "UCWEB/2.0(Java; U; MIDP-2.0; en-US; mozilla) U2/1.0.0 UCBrowser/8.8.1.252 U2/1.0.0 Mobile UNTRUSTED/1.0",
    "NokiaC1-01/2.0 (05.45) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; nokiac1-01) UCBrowser8.3.1.161/70/405/UCWEB Mobile",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 2.3.3; en-us ; LS670 Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1/UCBrowser/8.6.1.262/145/355",
    "Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; Microsoft; Lumia 535 Dual SIM) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537 UCBrowser/4.2.1.541 Mobile",
    "Mozilla/5.0 (S60V3; U; en-us; NokiaE75-1)/UC Browser8.5.0.183/28/352/UCWEB Mobile",
    "Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; vivo 1724 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.5.1146 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.2; en-US; Redmi 5A Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi Note 3 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.0.0.1088 Mobile Safari/537.36",
    "UCWEB/2.0(Symbian; U; S60 V3; en-US; NOKIAE5-00) U2/1.0.0 UCBrowser/8.8.0.245 U2/1.0.0 Mobile",
    "Nokia201/2.0 (11.81) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; nokia201) U2/1.0.0 UCBrowser/8.9.0.251 U2/1.0.0 Mobile",
    "NokiaC3-00/5.0 (08.65) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; kau; nokiac3-00) UCBrowser8.3.0.154/70/405/UCWEB Mobile",
    "Mozilla/5.0 (S60V5; U; en-us; NokiaC5-03)/UC Browser8.2.0.132/50/352/UCWEB Mobile",
    "BREW-Applet/0x20068888 (BREW/3.1.5.20; DeviceId: 90005; Lang: zhcn) ucweb-squid",
    "Mozilla/5.0 (Linux; U; Android 7.1.2; en-US; Redmi Note 5 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J210F Build/MMB29Q) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.4.5.1005 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 6.0; en-US; Redmi Note 4 Build/MRA58K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.4.2.995 U3/0.8.0 Mobile Safari/534.30",
    "UCWEB/2.0 (Windows; U; wds 10.0; en-US; Microsoft; RM-1099_1014) U2/1.0.0 UCBrowser/4.2.1.541 U2/1.0.0 Mobile",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; Lenovo A6020a40 Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.5.2.582 U3/0.8.0 Mobile Safari/534.30",
    "UCWEB/2.0 (Linux; U; Adr 2.3.5; en-US; TECNO_P3) U2/1.0.0 UCBrowser/8.2.0.242 U2/1.0.0 Mobile",
    "NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2;.NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2)/UC Browser7.9.0.102/70/352",
    "NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; kau; nokiac1-01) UCBrowser8.4.0.159/69/444/UCWEB Mobile UNTRUSTED/1.0",
    "UCWEB/2.0 (Linux; U; Opera Mini/7.1.32052/30.3697; ru; E15i Build/2.1.1.A.0.6) U2/1.0.0 UCBrowser/10.6.8.732 Mobile",
    "UCWEB/2.0 (Java; U; MIDP-2.0; Nokia203/20.37) U2/1.0.0 UCMini/11.3.0.1130 (SpeedMode; Proxy; Android 5.1; Lenovo_A2010-a ) U2/1.0.0 Mobile",
    "Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Redmi 6 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; en-US; MI MAX 2 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; x600 Build/ABXCNOP5902303111S) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.6.4) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
    "UCWEB/2.0 (Symbian; U; S60 V3; en-US; NokiaE71) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile",
    "Mozilla/5.0 (Linux; U; Android 5.0; en-US; Micromax Q355 Build/LRX21M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.8.0.718 U3/0.8.0 Mobile Safari/534.30",
    "NokiaX2-01/5.0 (07.10) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; kau; nokiax2-01) UCBrowser8.3.0.154/70/355/UCWEB Mobile",
    "Nokia200/2.0 (10.61) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0(Java; U; MIDP-2.0; en-us; nokia200) U2/1.0.0 UCBrowser/8.7.1.234 U2/1.0.0 Mobile",
    "Mozilla/5.0 (Linux; U; Android 5.0.2; en-US; HTC Desire 826 dual sim Build/LRX22G) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.7.2.645 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 7.1.2; en-US; Redmi 5A Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.5.1121 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-J701F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-J710F Build/NRD90M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.3.8.976 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J700F Build/LMY48B) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.3.0.950 U3/0.8.0 Mobile Safari/534.30",
    "UCWEB/2.0(Java; U; MIDP-2.0; en-us; generic) U2/1.0.0 UCBrowser/8.7.1.234 U2/1.0.0 Mobile",
    "Nokia311/5.0 (07.36) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; Nokia311) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile UNTRUSTED/1.0",
    "UCWEB/2.0 (Symbian; U; S60 V3; en-US; NokiaE63) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile",
    "NokiaC2-01/5.0 (11.00) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; nokiac2-01) U2/1.0.0 UCBrowser/8.9.0.251 U2/1.0.0 Mobile",
    "Nokia200/2.0 (10.58) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; kau; nokia200) UCBrowser8.2.0.132/70/352/UCWEB Mobile",
    "NokiaC6-00/UC Browser8.0.3.107/50/352/UCWEB",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.89 Safari/537.36 UCBrowser/11.3.5.908",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi Note 4 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J700F Build/LMY48B) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1; en-US; HTC Desire 728 dual sim Build/LMY47D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.3.0.950 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.10.8.820 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 4.1.2; en-US; GT-S7392 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.8.0.718 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.9.0.731 U3/0.8.0 Mobile Safari/534.30",
    "Nokia302/5.0 (14.78) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; Desktop) AppleWebKit/534.13 (KHTML, like Gecko) UCBrowser/9.5.0.449",
    "Mozilla/5.0 (Linux; U; Android 7.0; en-US; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.10.0.1163 Mobile Safari/537.36",
    "NOKIAE5-00/UC Browser8.0.4.121/28/444/UCWEB",
    "NokiaC3-00/5.0 (08.65) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; nokiac3-00) AppleWebKit/530.13 (KHTML, like Gecko) UCBrowser/8.5.0.185/83/352/UCWEB Mobile",
    "UCWEB/2.0 (Linux; U; Opera Mini/7.1.32052/30.3697; en-US; E15i) U2/1.0.0 UCBrowser/10.1.2.571 Mobile",
    "Mozilla/5.0 (Linux; U; Android 5.0.2; en-US; XT1032 Build/LXB22.46-28.1) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.2.0.535 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J111F Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; A37f Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.8.8.730 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 4A Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; A33f Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.3.8.976 U3/0.8.0 Mobile Safari/534.30",

    "Mozilla/5.0 (Linux; U; Android 6.0; en-US; Lenovo A7020a48 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.0.2; en-US; Lenovo A6000 Build/LRX22G) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.2.0.915 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.2.0.915 U3/0.8.0 Mobile Safari/534.30",
    "Opera/9.80 (Android; Opera Mini/7.28879/27.1662; U; en-us) Presto/2.8.119 Version/11.10 UCBrowser/8.4.1.204/145/444/",
    "UCWEB/2.0 (Symbian; U; S60 V3; id; NokiaN73) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile",
    "UCWEB/2.0(Symbian; U; S60 V3; en-US; NokiaC5-00.2) U2/1.0.0 UCBrowser/8.8.0.245 U2/1.0.0 Mobile",
    "Mozilla/5.0 (S60V5; U; en-us; NokiaC6-00)/UC Browser8.5.0.183/50/352/UCWEB Mobile",
    "NokiaC3-00/5.0 (07.20) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0(Java; U; MIDP-2.0; en-us; nokiac3-00) U2/1.0.0 UCBrowser/8.7.1.234 U2/1.0.0 Mobile",
    "Nokia200/2.0 (10.60) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; nokia200) U2/1.0.0 UCBrowser/8.9.0.251 U2/1.0.0 Mobile",
    "Nokia302/5.0 (14.53) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; nokia302) AppleWebKit/530.13 (KHTML, like Gecko) UCBrowser/8.6.0.199/69/352/UCWEB Mobile UNTRUSTED/1.0",
    "Nokia2690/2.0 (10.10) Profile/MIDP-2.1 Configuration/CLDC-1.1 nokia2690/UC Browser7.4.0.65/69/352 UNTRUSTED/1.0",
    "UCWEB/2.0(Symbian; U; S60 V3; en-US; NokiaC5-00) U2/1.0.0 UCBrowser/8.8.1.252 U2/1.0.0 Mobile",
    "Nokia200/2.0 (10.61) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; kau; nokia200) UCBrowser8.2.1.144/70/355/UCWEB Mobile",
    "Mozilla/5.0 (Linux; U; Android 4.1.1; en-us; GT-P3100B Build/JRO03C) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.8.0.435 U3/0.8.0 Mobile Safari/533.1",
    "UCWEB/2.0 (Java; U; MIDP-2.0; Nokia203/20.37) U2/1.0.0 UCMini/11.0.6.1040 (SpeedMode; Proxy; Android 6.0.1; SM-J510FN ) U2/1.0.0 Mobile",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 3S Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 3S Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi Note 4 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J210F Build/MMB29Q) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.2.8.945 U3/0.8.0 Mobile Safari/534.30",
    "LG/GT505/v10a Browser/Teleca-Q7.1 MMS/LG-MMS-V1.0/1.2 MediaPlayer/LGPlayer/1.0 Java/ASVM/1.1 Profile/MIDP-2.1 Configuration/CLDC-1.1 UNTRUSTED/1.0 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; lg) U2/1.0.0 UCBrowser/8.9.0.251 U2/1.0.0 Mobile",
    "Nokia206/2.0 (04.52) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; Nokia206) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile UNTRUSTED/1.0",
    "Mozilla/5.0 (Linux; U; Android 5.1; en-us; Lenovo A2010-a Build/LMY47D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/534.30",
    "Nokia311/5.0 (07.36) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; Nokia311) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile",
    "NokiaC3-01/5.0 (05.65) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; nokiac3-01) AppleWebKit/530.13 (KHTML, like Gecko) UCBrowser/8.6.0.199/70/352/UCWEB Mobile UNTRUSTED/1.0",
    "Nokia200/2.0 (11.64) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; nokia200) U2/1.0.0 UCBrowser/8.9.0.251 U2/1.0.0 Mobile",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2;.NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2) UCBrowser/8.6.0.199/69/352 UNTRUSTED/1.0",
    "Mozilla/5.0 (Linux; U; Android 4.4.4; en-US; SM-G316HU Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.5.2.582 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/12B466 UCBrowser/10.7.11.672 Mobile",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J500F Build/LMY48B) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.4.2.995 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1; en-US; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI NOTE LTE Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.6.4) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.2.0.915 U3/0.8.0 Mobile Safari/534.30",
    "UCWEB/2.0 (Windows; U; wds 10.0; en-IN; Microsoft; RM-1067_1005) U2/1.0.0 UCBrowser/4.2.1.541 U2/1.0.0 Mobile",
    "Mozilla/5.0 (Linux; U; Android 4.1.2; en-US; GT-S7262 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.9.0.731 U3/0.8.0 Mobile Safari/534.30",
    "Nokia114/2.0 (03.33) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; nokia114) U2/1.0.0 UCBrowser/9.2.0.311 U2/1.0.0 Mobile",
    "Mozilla/5.0 (Linux; U; Android 4.4.4; en-us; Lenovo A6000 Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.7.5.418 U3/0.8.0 Mobile Safari/533.1",
    "UCWEB/2.0 (Linux; U; Adr 2.1-update1; en-US; SGH-T959) U2/1.0.0 UCBrowser/8.2.0.242 U2/1.0.0 Mobile",
    "Mozilla/5.0 (S60V3; U; en-us; NOKIAE5-00)/UC Browser8.2.0.132/28/355/UCWEB Mobile",
    "Mozilla/5.0 (S60V3; U; en-us; NOKIAE5-00)/UC Browser8.2.0.132/28/444/UCWEB Mobile",
    "NokiaX2-01/5.0 (08.70) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0(Java; U; MIDP-2.0; en-US; nokiax2-01) U2/1.0.0 UCBrowser/8.8.1.252 U2/1.0.0 Mobile",
    "Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; R829 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.9.0.731 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-A500G Build/MMB29M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.2.8.945 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 UCBrowser/10.7.9.856 Mobile",
    "Mozilla/5.0 (Linux; U; Android 5.1; en-US; P5L Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.5.1121 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; vivo Xplay5A Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.6.4) WindVane/8.0.0 1440X2560 GCanvas/1.4.2.21",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.0.0.1088 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J210F Build/MMB29Q) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.2.0.915 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1; en-US; Lenovo P1ma40 Build/LMY47D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.2.0.915 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; TECNO M5 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30",
    "UCWEB/2.0 (Linux; U; Adr 2.3.6; en-AE; HUAWEI_Y210-0200) U2/1.0.0 UCBrowser/8.6.0.276 U2/1.0.0 Mobile",
    "Mozilla/5.0 (Linux; U; Android 4.4.4; en-US; SM-G360H Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.2.0.535 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; SM-G610F Build/M1AJQ) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.10.0.1163 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.2; en-US; Redmi Note 5 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.10.1159 Mobile Safari/537.36",
    "Nokia200/2.0 (10.60) Profile/MIDP-2.1 Configuration/CLDC-1.1 nokia200/UC Browser8.0.3.107/70/355",
    "Mozilla/5.0 (Linux; U; Android 2.3.5; en-US; TECNO N3 Build/master) AppleWebKit/534.31 (KHTML, like Gecko) UCBrowser/9.0.2.299 U3/0.8.0 Mobile Safari/534.31",
    "Mozilla/5.0 (Java; U; en-us; 11a h700tecno) AppleWebKit/530.13 (KHTML, like Gecko) UCBrowser/8.5.0.185/82/405/UCWEB Mobile UNTRUSTED/1.0",
    "Mozilla/5.0 (Linux; U; Android 4.4.4; en-US; SM-G7202 Build/KTU84P) AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 UCBrowser/10.7.5.785 Mobile",
    "Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; GT-S7272 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.8.855 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; SM-N900 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.1.0.882 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 6.0; en-US; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.5.1121 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1; en-US; Quattro L55 HD Build/LMY47D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.7.2.645 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X; en-US) AppleWebKit/601.1.46.45.1 (KHTML, like Gecko) Mobile/13C75 UCBrowser/9.3.0.326 Mobile",
    "Mozilla/5.0 (Linux; U; Android 8.0.0; en-US; Lenovo K8 Note Build/OMB27.43-62) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.8.1140 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.5.1121 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J500F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; A37fw Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.0; en-US; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36",
    "UCWEB/2.0 (Symbian; U; S60 V3; en-US; NOKIA6120c) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile",
    "UCWEB/2.0(Symbian; U; S60 V3; en-US; NokiaE71) U2/1.0.0 UCBrowser/8.8.1.252 U2/1.0.0 Mobile",
    "NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; nokiac1-01) UCBrowser8.4.0.159/69/352/UCWEB Mobile UNTRUSTED/1.0",
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us ; GT-I9001 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1/UCBrowser/8.5.1.235/145/355",
    "NokiaC6-00/UC Browser7.7.1.88/50/444",
    "Nokia5130c-2/2.0 (07.91) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; kau; nokia5130c-2) UCBrowser8.3.0.154/70/355/UCWEB Mobile",
    "NokiaX2-01/5.0 (08.65) Profile/MIDP-2.1 Configuration/CLDC-1.1 nokiax2-01/UC Browser7.9.0.102/70/352 UNTRUSTED/1.0",
    "NokiaX2-05/2.0 (08.60) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; nokiax2-05) UCBrowser8.3.1.161/69/355/UCWEB Mobile",
    "Nokia2700c-2/2.0 (09.97) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; kau; nokia2700c-2) UCBrowser8.4.0.159/69/444/UCWEB Mobile UNTRUSTED/1.0",
    "NokiaC3-00/5.0 (07.20) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; nokiac3-00) AppleWebKit/530.13 (KHTML, like Gecko) UCBrowser/8.6.0.199/69/444/UCWEB Mobile UNTRUSTED/1.0",
    "Nokia200/2.0 (11.64) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; nokia200) AppleWebKit/530.13 (KHTML, like Gecko) UCBrowser/8.6.0.199/70/444/UCWEB Mobile",
    "NokiaN70-1/5.0737.3.0.1 Series60/2.8 Profile/MIDP-2.0 Configuration/CLDC-1.1/UC Browser7.9.1.120/27/352/UCWEB",
    "Mozilla/5.0 (Linux; U; Android 5.1; en-US; P3S Build/LMY47I) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.9.878 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J510FN Build/MMB29M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.8.0.718 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; LS-5010 Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; ZUK Z1 Build/LMY49J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.10.8.820 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; Z1 Build/LMY49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-T331 Build/LMY47X) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.10.5.809 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; GT-I9515 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.5.0.575 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 7.1.2; en-US; Redmi 5A Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.9.1155 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.2.1143 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.0; en-US; XT1663 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.2.0.1089 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.0; en-US; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.7.1153 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J210F Build/MMB29Q) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.4.2.995 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.0; ar-SA; Lenovo A1000 Build/S100) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.1.0.527 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; Redmi Note 3 Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.1.0.882 U3/0.8.0 Mobile Safari/534.30",
    "Nokia200/2.0 (11.81) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; nokia200) U2/1.0.0 UCBrowser/8.9.0.251 U2/1.0.0 Mobile UNTRUSTED/1.0",
    "Mozilla/5.0 (S60V3; U; en-us; NokiaE63)/UC Browser8.5.0.183/28/352/UCWEB Mobile",
    "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; GN3001 Build/LMY47I) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.7.0) WindVane/8.0.0 720X1280 GCanvas/1.4.2.21",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Coolpad 3600I Build/MMB29M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.10.5.809 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 6.0; en-US; XT1706 Build/MRA58K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1; en-US; Lenovo A2010-a Build/LMY47D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.7.5.658 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; Moto G (4) Build/NPJS25.93-14-18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; Moto G (5)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/70.0.3538.75 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (Linux; U) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; Moto G (5S) Plus Build/NPSS26.116-64-11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/68.0.3440.83 Mobile/15G77 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1.1; SlimTab7_3GR Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1.1; SM-J120M Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; SM-J710MN Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
]


#  传入图书详情页url，获取作者、出版社、前5条评论
def get_info_from_detail_page(url, book_url):
    headers = {
        "user-agent": random.choice(ua_list),
        "referer": url
    }
    response = requests.get(book_url, headers=headers, timeout=20)

    # 为什么要多次请求？如果一次请求失败，那就会取爬下一条图书，会导致top250中前100图书顺序出错
    if response.status_code != 200:
        print("第一次请求详情页：{}失败，第二次请求".format(book_url))
        time.sleep(random.uniform(20, 30))
        response = requests.get(book_url, headers=headers, timeout=20)

        if response.status_code != 200:
            print("第二次请求详情页：{}失败，第三次请求".format(book_url))
            time.sleep(random.uniform(30, 40))
            response = requests.get(book_url, headers=headers, timeout=20)

    response.encoding = "utf-8"

    tree = etree.HTML(response.text)

    # 获取出版社
    # 由于出版社名称不在任何标签中，例如：
    #  <span class="pl">出版社:</span> 上海人民出版社<br/>
    # 所以通过获取 <div id="info" class="">标签下所有文字组成的数组，
    text = tree.xpath('//*[@id="info"]//text()')

    text = " ".join(text)

    text = re.sub('\s+', ' ', text).strip()
    # 得到的结果如：作者: [美] 丹·布朗 出版社: 上海人民出版社 原作名: The Da Vinci Code 译者: 朱振武 / 吴晟 / 周元晓 出版年: 2004-2 页数: 432 定价: 28.00元 装帧: 平装 ISBN: 9787208050037

    # 提取出 作者: [美] 丹·布朗 出版社
    author_text = re.search("作者.*\w* 出版社", text).group(0)

    author = author_text.replace("作者", "").replace("：", "").replace(":", "").replace("出版社", "").strip()

    # print(text)
    # 提取出 出版社: 上海人民出版社
    publisher_text = re.search("出版社.*\w* +?", text).group(0)

    # print(text)
    # 截取出  上海人民出版社
    publisher = publisher_text.split(" ")[1]

    # 获取前5条评论
    li_list = tree.xpath('//*[@id="comments"][1]/ul/li')

    if li_list is None:
        print("解析评论所在的li数组失败......")
        return

    if len(li_list) == 0:
        print("评论所在的li数组长度为0......")
        return

    comment_list = []
    for li in li_list:
        comment = li.xpath('./div[@class="comment"]//p/span/text()')
        if comment is not None:
            comment = ' '.join(comment)
            comment = re.sub('\s+', ' ', comment).strip()
            comment_list.append(comment)

    return author, publisher, comment_list


def main():
    for i in range(len(url_list)):

        print("################# 爬取第{}页开始 ################".format(i))

        headers = {
            "user-agent": random.choice(ua_list),
            "referer": r"https://book.douban.com/"
        }

        response = None

        response = requests.get(url_list[i], headers=headers, timeout=20)

        # 如果请求失败，就再次发请求
        if response.status_code != 200:
            print("第一次请求分页{}：{}失败，第二次请求".format(i, url_list[i]))
            time.sleep(random.uniform(20, 30))
            response = requests.get(url_list[i], headers=headers, timeout=20)

            if response.status_code != 200:
                print("第二次请求分页{}：{}失败，第三次请求".format(i, url_list[i]))
                time.sleep(random.uniform(30, 40))
                response = requests.get(url_list[i], headers=headers, timeout=20)

        response.encoding = "utf-8"

        tree = etree.HTML(response.text)

        table_list = tree.xpath('//*[@id="content"]//table')

        if table_list is None:
            print("解析页面中书籍列表所在的table数组失败......")
            return

        if len(table_list) == 0:
            print("解析到的页面中书籍列表所在的table数组长度为0......")
            return

        for table in table_list:

            # 获取书名
            title = table.xpath('.//td[2]/div/a/text()')
            if title is not None:
                title = ''.join(title)
                # 移除所有空格
                title = title.replace('\r\n', '').replace('\n', '').replace('\r', '').replace('\t', '').strip()
                print("书名：", title)

            # 获取图书详情url
            book_url = table.xpath('.//td[2]/div/a/@href')
            if book_url is not None:
                book_url = "".join(book_url)
                print("图书详情url：", book_url)

            # 获取封面url
            img_url = table.xpath('.//td[1]/a/img/@src')
            if img_url is not None:
                img_url = "".join(img_url)
                print("封面url：", img_url)

            time.sleep(random.uniform(5, 10))

            author, publisher, comment_list = get_info_from_detail_page(url_list[i], book_url)
            print("作者：", author)
            print("出版社：", publisher)
            print("评论：", comment_list)
            print()
            print()

            data = []
            data.append((book_url, title,
                         author, publisher, img_url,
                         comment_list[0], comment_list[1], comment_list[2],
                         comment_list[3], comment_list[4]))
            cursor.executemany(sql, data)
            connection.commit()
            data.clear()

            time.sleep(random.uniform(10, 20))

        time.sleep(random.uniform(20, 30))

        print("################# 爬取第{}页结束 ################".format(i))

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
