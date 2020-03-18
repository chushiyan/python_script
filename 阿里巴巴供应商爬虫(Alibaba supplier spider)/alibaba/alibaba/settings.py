# -*- coding: utf-8 -*-

# Scrapy settings for alibaba project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'alibaba'

SPIDER_MODULES = ['alibaba.spiders']
NEWSPIDER_MODULE = 'alibaba.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'alibaba (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Default requests serializer is pickle, but it can be changed to any module
# with loads and dumps functions. Note that pickle is not compatible between
# python versions.
# Caveat: In python 3.x, the serializer must return strings keys and support
# bytes as values. Because of this reason the json or msgpack module will not
# work by default. In python 2.x there is no such issue and you can use
# 'json' or 'msgpack' as serializers.
SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"

# Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True

# Schedule requests using a priority queue. (default)
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

# Alternative queues.
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'

# Max idle time to prevent the spider from being closed when distributed crawling.
# This only works if queue class is SpiderQueue or SpiderStack,
# and may also block the same time when your spider start at the first time (because the queue is empty).
# SCHEDULER_IDLE_BEFORE_CLOSE = 10


# 指定redis数据库的连接参数
# REDIS_PASS是我自己加上的redis连接密码（默认不做）
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
# REDIS_PASS = 'redisP@ssw0rd'

# LOG等级
LOG_LEVEL = 'DEBUG'

# 默认情况下,RFPDupeFilter只记录第一个重复请求。
# 将DUPEFILTER_DEBUG设置为True会记录所有重复的请求。
# DUPEFILTER_DEBUG = True


# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
#     'referer': 'https://s.1688.com',
# }
# DEFAULT_REQUEST_HEADERS = {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "accept-encoding": "gzip, deflate, br",
#     "accept-language": "zh-CN,zh;q=0.9",
#     "cache-control": "max-age=0",
#     "cookie": 'UM_distinctid=16aba5157e62d1-0359e3c1b13207-9333061-75300-16aba5157e72ce; ali_ab=14.156.203.41.1557904055940.5; cna=t6hiFZsfxgYCAQ6cyykfddO2; cookie2=1622e6fadee4a2726766735c4fac5947; t=2669c788eb4404ed3c9b6ba9c3da7f95; _tb_token_=7e66353331e3b; __wapcsf__=1; cookie1=VFCpy7iSLSOHVJ57Vj3cMjs6BNE%2Fy1idhNrVqlD1Wog%3D; cookie17=UNDXnNWLbyZ8aQ%3D%3D; sg=%E9%92%A727; csg=1bd6f6e8; lid=%E8%B1%AB%E7%AB%A0%E9%83%A1%E8%92%8B%E5%A3%AB%E9%92%A7; unb=3031735292; __cn_logon__=true; __cn_logon_id__=%E8%B1%AB%E7%AB%A0%E9%83%A1%E8%92%8B%E5%A3%AB%E9%92%A7; ali_apache_track=c_mid=b2b-30317352921582c|c_lid=%E8%B1%AB%E7%AB%A0%E9%83%A1%E8%92%8B%E5%A3%AB%E9%92%A7|c_ms=1; ali_apache_tracktmp=c_w_signed=Y; _nk_=%5Cu8C6B%5Cu7AE0%5Cu90E1%5Cu848B%5Cu58EB%5Cu94A7; last_mid=b2b-30317352921582c; _csrf_token=1557904135816; _is_show_loginId_change_block_=b2b-30317352921582c_false; _show_force_unbind_div_=b2b-30317352921582c_false; _show_sys_unbind_div_=b2b-30317352921582c_false; _show_user_unbind_div_=b2b-30317352921582c_false; __rn_alert__=false; alicnweb=homeIdttS%3D80122438648200925281646457486999404179%7Ctouch_tb_at%3D1557904059237%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3D%25E8%25B1%25AB%25E7%25AB%25A0%25E9%2583%25A1%25E8%2592%258B%25E5%25A3%25AB%25E9%2592%25A7; ad_prefer="2019/05/15 15:09:28"; h_keys="usb%u98ce%u6247"; l=bBQxJbRuvVebH37tBOCg5uI8ai_tIIRAguPRwN4Mi_5QJOTsTu7OldqAyH96VjfRs08Bq-L8Y1J9-etkA; isg=BBAQ2pzeeEh9lCRMAGi3Akgv4V6icfQvOxkFTgrh2ms-RbDvsuk6s3R9GUwAlaz7',
#     "upgrade-insecure-requests": 1,
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'alibaba.middlewares.AlibabaSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'alibaba.middlewares.RotateUserAgentMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'alibaba.pipelines.NoSpacePipeline':200,
    'alibaba.pipelines.JSONPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 10
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 180
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
