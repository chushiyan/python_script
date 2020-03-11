# 爬取妹子图网站的图片    2019年1月10日17:37:37
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import os
import re
import datetime
import http.cookiejar
import time
import socket
import sys

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class MzituSpider(object):
    # # 起始页
    # start_page_str
    #
    # # 结束页
    # end_page_str
    #
    # group_count = 0
    #
    # image_count = -4  # 扣除四个日志文件
    #
    # # 组图的url的列表
    # group_url_list = []
    #
    # # 组图的标题
    # group_title_list = []
    #
    # # 妹子图网站目前总共206页，每页24组 图片（最后一页未必是24组）
    # # 在当前目录创建meizitu目录保存所有爬取的图片，里面又以组图标题为名的文件夹
    # # 实现的目录结构如： ./meizitu-page001-002/组图标题/图片
    #
    # # 根目录
    # root_dir_name
    # root_dir_path
    #
    # # ---------- 文件1 -----------
    # # 爬虫info日志文件
    # info_file
    #
    # # ---------- 文件2 -----------
    # # 爬虫error日志文件
    # error_file
    #
    # # ---------- 文件3 -----------
    # # 保存 抓取失败了的图片的信息的 文件
    # reload_file

    def __init__(self, start_page_str, end_page_str):
        self.start_page_str = start_page_str
        self.end_page_str = end_page_str

        self.init_file()

        # 指定 请求失败后，最多再发几次请求
        self.REQUEST_COUNT = 8

        # 当前对同一url发了几次请求
        self.current_request_count = 0

        self.group_url_list = []
        self.group_title_list = []
        self.group_count = 0
        self.image_count = -4  # 扣除四个日志文件

        self.headers = {
            # ":authority": "www.mzitu.com",
            # ":method": "GET",
            # ":path": "/",
            # ":scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            # "cache-control": "max-age=0",
            # "cookie": "Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1547104670; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1547105012",
            "referer": "https://www.mzitu.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
        self.cookiejar = http.cookiejar.CookieJar()
        self.handler = urllib.request.HTTPCookieProcessor(self.cookiejar)
        self.opener = urllib.request.build_opener(self.handler)

    def init_file(self):

        if self.start_page_str == self.end_page_str:
            self.root_dir_name = "meizitu" + "-page" + self.start_page_str
        else:
            self.root_dir_name = "meizitu" + "-page" + self.start_page_str + "-" + self.end_page_str

        self.root_dir_path = os.path.join(os.getcwd(), self.root_dir_name)

        if not os.path.exists(self.root_dir_path):
            os.mkdir(self.root_dir_path)

        # ---------- 文件1 -----------
        # 爬虫info日志文件
        self.info_file = open(os.path.join(self.root_dir_path, "info.log"), "a", encoding="utf-8")

        # ---------- 文件2 -----------
        # 爬虫error日志文件
        self.error_file = open(os.path.join(self.root_dir_path, "error.log"), "a", encoding="utf-8")

        # ---------- 文件3 -----------
        # 保存 抓取失败了的图片的信息的 文件
        self.reload_file = open(os.path.join(self.root_dir_path, "reload.txt"), "a+", encoding="utf-8")

        # 具体执行请求的函数
    def request_and_response(self, url, img_path):
            self.current_request_count += 1
            if self.REQUEST_COUNT < self.current_request_count:
                # 需要减1，因为上两行加了1，但实际上到下面这行为止，并没有真正再次请求
                print(url + "  第%d次请求失败，不再发起请求" % (self.current_request_count - 1))
                self.current_request_count = 0
                return None
            try:
                print(url + "  发起第%d次请求" % (self.current_request_count))
                request = urllib.request.Request(url=url, headers=self.headers)
                response = self.opener.open(request, timeout=6)
            except Exception as e:
                print(e)
                print(url + "  第%d次请求失败" % (self.current_request_count))
                time.sleep(self.current_request_count * 2)
                self.request_and_response(url)
            else:
                print(url + "  第%d次请求成功" % (self.current_request_count))
                self.current_request_count = 0
                return response

    # 具体执行请求的函数
    def request_and_response2(self, url, img_path):
        response = ""

        def get_response():
            request = urllib.request.Request(url=url, headers=self.headers)
            return self.opener.open(request, timeout=6)
        try:
            response = get_response()
        except Exception as e:
            print(e)
            time.sleep(5)
            print("第1次请求%s失败，发起第2次请求....." % (url))
            try:
                response = get_response()
            except Exception as e:
                print(e)
                time.sleep(5)
                print("第2次请求%s失败，发起第3次请求....." % (url))
                try:
                    response = get_response()
                except Exception as e:
                    print(e)
                    time.sleep(10)
                    print("第3次请求%s失败，发起第4次请求....." % (url))
                    try:
                        response = get_response()
                    except Exception as e:
                        print(e)
                        time.sleep(20)
                        print("第4次请求%s失败，发起第5次请求....." % (url))
                        try:
                            response = get_response()
                        except Exception as e:
                            print(e)
                            time.sleep(20)
                            print("第5次请求%s失败，发起第6次请求....." % (url))
                            try:
                                response = get_response()
                            except Exception as e:
                                print(e)
                                time.sleep(20)
                                print("第6次请求%s失败，发起第7次请求....." % (url))
                                try:
                                    response = get_response()
                                except Exception as e:
                                    print(e)
                                    time.sleep(20)
                                    print("第7次请求%s失败，发起第8次请求....." % (url))
                                    try:
                                        response = get_response()
                                    except Exception as e:
                                        print(e)
                                        if not img_path == None:
                                            self.error_file.write(url + "@@@@@" + img_path + "\n")
                                        else:
                                            self.error_file.write(url + "@@@@@" + "\n")

        return response

    # ----------------  函 数 ----------------
    # 从首页上爬取组图的url，下载图片
    def run(self):
        # https://www.mzitu.com/page/1/  等于https://www.mzitu.com
        # https://www.mzitu.com/page/2/
        # https://www.mzitu.com/page/3/
        final_url = r"https://www.mzitu.com/page/"

        for i in range(int(self.start_page_str), int(self.end_page_str) + 1):

            index_url = final_url + str(i) + "/"

            print("-" * 30)
            print(index_url)
            print("-" * 30)

            print("#########################################")
            print("...........第%d页中的组图爬取开始.........." % i)
            print("#########################################")

            self.info_file.write("#########################################\n")
            self.info_file.write("...........第%d页中的组图爬取开始..........\n" % i)
            self.info_file.write("#########################################\n")

            # 2019-01-11 10:39:13.470375  去掉后面的小数
            self.info_file.write(str(datetime.datetime.now()).split(".")[0] + "\n")

            try:
                response = self.request_and_response(index_url, None)
                soup = BeautifulSoup(response.read(), "lxml")
                lis = soup.find("ul", {"id": "pins"}).findAll("li")

                # 遍历所有li，从中拿到组图的url / title
                for li in lis:

                    if li['class']:
                        continue

                    url = li.span.a["href"]  # 如：https://www.mzitu.com/164690

                    self.group_url_list.append(url)

                    title = li.span.a.get_text()  # 如：深航美女空姐九尾Ivy丝袜玉足性感极致

                    #  不能用于windows文件名的字符：  \/:*?"<>|
                    # 替换掉标题中可能存在的不能用于windows文件名的字符
                    title = re.sub(r"[!！@#$%^&~\\\/\:\*\?\"<>|,]", " ", title)

                    # 实际中出现：
                    # 原标题：你要车,还是要人?
                    # 系统找不到指定的路径:  你要车 还是要人 \\201306213444wtdflw1dolv.jpg
                    title = title.strip()

                    self.group_title_list.append(title)

                    print(url)
                    print(title)
                    print("")

                currentPage = i
                self.get_images_url(currentPage)

                # 清空一下：
                # 组图的url的列表
                self.group_url_list.clear()

                # 组图的标题
                self.group_title_list.clear()

                time.sleep(1)

            except Exception as e:
                print(e)

            print("#########################################")
            print("...........第%d页中的组图爬取结束.........." % i)
            print("#########################################")

            self.info_file.write("#########################################\n")
            self.info_file.write("...........第%d页中的组图爬取结束..........\n" % i)
            self.info_file.write("#########################################\n")

            # 2019-01-11 10:39:13.470375  去掉后面的小数
            self.info_file.write(str(datetime.datetime.now()).split(".")[0] + "\n")

    # ---------------- 函 数 ----------------
    # 从group_url_list组图的url中获取每组中的各个图片
    def get_images_url(self, currentPage):
        time.sleep(1)

        for i in range(len(self.group_url_list)):

            currentGroup = i + 1

            print("-" * 50)
            print(".....正在爬取第%s页中的第%s组图片....." % (currentPage, currentGroup))
            print(self.group_title_list[i])
            print("-" * 50)

            self.info_file.write("-" * 50 + "\n")
            self.info_file.write("正在爬取第%s页中的第%s组图片....." % (currentPage, currentGroup) + "\n")
            self.info_file.write(self.group_title_list[i] + "\n")
            self.info_file.write("-" * 50 + "\n\n")

            #  实现的目录结构： ./meizitu/组图标题/图片
            group_path = os.path.join(self.root_dir_path, self.group_title_list[i])

            if not (os.path.exists(group_path)):
                os.mkdir(group_path)

            currentImage = 1
            img_url_list = []

            # 比如：https://www.mzitu.com/165947这组图总共50涨，
            # 当访问https://www.mzitu.com/165947/51 及以上时不会报错，
            # 而是跳转到https://www.mzitu.com/165947/1
            # 跳出循环的条件：上一页面中图片的url和当前页面中图片url相同

            while True:

                # 如：https://www.mzitu.com/165947
                # 需要加上字符，变成如：https://www.mzitu.com/165947/1
                group_paging_url = self.group_url_list[i] + "/" + str(currentImage)

                img_path = ""
                img_url = ""

                try:
                    soup = BeautifulSoup(self.request_and_response(group_paging_url, None).read(), "lxml")
                    img_url = soup.find("div", {"class": "main-image"}).img["src"]

                    if img_url in img_url_list:
                        break
                    img_url_list.append(img_url)

                    print(img_url)
                    self.info_file.write(img_url + "\n")
                    img_path = os.path.join(group_path, img_url.split("/")[-1])

                    self.down_images(self.request_and_response(img_url, img_path), img_path, img_url, currentPage,
                                     currentGroup,
                                     currentImage)

                except Exception as e:
                    print(e)

                currentImage += 1

            img_url_list.clear()
            self.info_file.flush()
            self.error_file.flush()
            self.reload_file.flush()

            time.sleep(1)

    def down_images(self, response, img_path, img_url, currentPage, currentGroup, currentImage):
        try:
            with open(img_path, "wb") as f:
                f.write(response.read())
        except Exception as e:
            print(e)
            self.info_file.write("第%s页 第%s组 第%s张图 保存失败....." % (currentPage, currentGroup, currentImage) + "\n\n")
            self.error_file.write(self.group_title_list[currentGroup - 1] + "\n")
            self.error_file.write("第%s页 第%s组 第%s张图 保存失败....." % (currentPage, currentGroup, currentImage) + "\n\n")
            self.error_file.write("\n")

            self.reload_file.write(img_url + "@@@@@" + self.group_title_list[currentGroup - 1] + "\n")
        else:
            self.info_file.write("第%s页 第%s组 第%s张图 保存成功....." % (currentPage, currentGroup, currentImage) + "\n\n")

    # ------------  函 数 ------------
    # 结果统计
    def summarize_result(self):
        def get_dir_file_count(path):

            dir_file_list = os.listdir(path)

            for i in range(len(dir_file_list)):
                dir_or_file_name = dir_file_list[i]
                dir_or_file_path = os.path.join(self.root_dir_path, dir_or_file_name)
                if os.path.isdir(dir_or_file_path):
                    self.group_count += 1
                    get_dir_file_count(dir_or_file_path)
                else:
                    self.image_count += 1

        get_dir_file_count(self.root_dir_path)
        result = "组图数量：%d\n" % (self.group_count)
        result += "图片数量：%d\n" % (self.image_count)

        return result

    # ------------  函 数 ------------
    # 发送邮件
    def send_email(self, my_title, my_msg):
        # ------ 一、连接SMTP服务器（就像打开163邮箱网页一样）-------
        # SMTP服务器，（此处是网易的）
        SMTPServer = "smtp.163.com"

        # 创建SMTP服务器（其实是连上SMTP服务器），25是端口号
        mailServer = smtplib.SMTP(SMTPServer, 25)

        # ---- 二、登录邮箱账号（就像在163邮箱网页输入账号密码登录）----
        # 发件人的邮箱
        sender = "KnightChu1314@163.com"

        # 发件人的授权码
        password = "CHU828shi1314"

        # 登录
        mailServer.login(sender, password)

        # --------------------- 三、编写邮件内容 ---------------------
        # 设置邮件内容
        msg = my_msg

        # 转换成邮件文本
        msg = MIMEText(msg)

        # 设置邮件标题
        msg["Subject"] = my_title

        # 设置发件人
        msg["From"] = sender

        # -------------------- 四、发送邮件 --------------------
        mailServer.sendmail(sender, ["chushiyan0415@163.com"], msg.as_string())

        # --------------------- 五、退出邮箱 --------------------
        mailServer.quit()

        '''注意：
        有时候会发生554 DT:SPM错误，这时要修改邮件内容
            •554 DT:SPM 发送的邮件内容包含了未被许可的信息，或被系统识别为垃圾邮件。请检查是否有用户发送病毒或者垃圾邮件；
        	网易/企业退信的常见问题？ http://help.163.com/09/1224/17/5RAJ4LMH00753VB8.html
        '''


if __name__ == "__main__":
    start_time = time.time()
    start_full_time = datetime.datetime.now().__str__().split(".")[0]
    start_page_str = None
    end_page_str = None

    try:
        init_file = open(os.path.join(os.getcwd(), "init.property"), "r", encoding="utf-8")
        start_page_str = init_file.readline().split("=")[-1].strip()
        end_page_str = init_file.readline().split("=")[-1].strip()

        init_file.close()
    except Exception as e:
        print(e)
        print("程序初始化失败")
        print("请检查配置文件init.property是否存在，以及是否配置正确")
        print("程序退出")
        sys.exit(0)

    spider = MzituSpider(start_page_str, end_page_str)

    try:
        spider.run()
    except Exception as e:
        print(e)
        result = ""
        result += "主机名：" + socket.gethostname() + "\n"
        result += "起始页：" + spider.start_page_str + "\n"
        result += "结束页：" + spider.end_page_str + "\n"
        print(result)
        spider.send_email("程序发生异常" + datetime.datetime.now().__str__().split(".")[0], result)

    spider.info_file.close()
    spider.error_file.close()
    spider.reload_file.close()

    print("睡眠10秒中.........以便结束读写操作")
    time.sleep(10)
    print("所有文件关闭")

    end_time = time.time()

    # 秒换算成 00:00:00格式
    seconds = end_time - start_time
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    print("程序总耗时：%02d:%02d:%02d" % (h, m, s))
    try:
        result = ""
        result += "主机名：" + socket.gethostname() + "\n"
        result += "程序开始时间：" + start_full_time + "\n"
        result += "程序结束时间：" + datetime.datetime.now().__str__().split(".")[0] + "\n"
        result += "程序耗时：%02d:%02d:%02d" % (h, m, s) + "\n"
        result += "起始页：" + spider.start_page_str + "\n"
        result += "结束页：" + spider.end_page_str + "\n"
        result += spider.summarize_result()
        print(result)
        spider.send_email("程序运行结果统计" + datetime.datetime.now().__str__().split(".")[0], result)
    except Exception as e:
        print(e)
        print("邮件发送失败")
    else:
        print("邮件发送成功")

    print("程序结束")
