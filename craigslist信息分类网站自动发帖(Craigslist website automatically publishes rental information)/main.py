# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Create By chushiyan@163.com
import requests
import time, random
from bs4 import BeautifulSoup

# 创建会话对象，
session = requests.Session()

# craigslist account's email & password

EMAIL = ""

PSW = ""

import datetime

BASE_URL = "https://www.homadorma.com/en/homestay/HS10"

homadorma_url = None

movein_date = ""


# 获取Homadorma网站一个随机url中的Available From
def getAvailableFrom():
    def genRandomHomadormaUrl():
        num_list = random.choices("0123456789", k=4)
        random_num = "".join(num_list)
        print("生成的随机4位数：", random_num)
        url = BASE_URL + random_num
        print("生成的随机URL：", url)
        headers = {
            "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": r"https://www.homadorma.com/",
            "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        }
        response = requests.get(url, headers=headers, timeout=6)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")
        # h4 = soup.find("h4", {"class": "center-align"}, text="Oops!")
        h4 = soup.find("h4", text="Oops!")

        # 如果解析到 页面存在 文字为Oops!的h4标签，说明该url无效，再次生成url、发请求
        if h4 is not None:
            genRandomHomadormaUrl()

        return url, h4, soup

    url, h4, soup = genRandomHomadormaUrl()

    date_str = soup.find("p", {"style": "margin: 5px 0 5px 10px;"}).get_text()
    print(type(date_str))

    date_str = date_str.split(':')[1].replace('\r\n', '').replace('\n', '').replace('\r', '').replace('\t', '').strip()
    # 如：March 24, 2020
    print(date_str)
    return url, date_str


# 日期格式转换，由March 14, 2020 这种格式转成 2020-03-14格式
def formatDate(date_str):
    # w=datetime.datetime.strptime("March 14, 2020", "%B %d, %Y").strftime('%Y-%m-%d')
    w = datetime.datetime.strptime(date_str, "%B %d, %Y").strftime('%Y-%m-%d')
    # print(w)
    return w


# 循环获取 已经格式化的Available From（由March 14, 2020 这种格式转成 2020-03-14格式），
# 直到获取到一个正确的结束
def getFormatedgetAvailableFrom():
    global homadorma_url, movein_date
    while True:
        try:
            homadorma_url, date_str = getAvailableFrom()
        except Exception as e:
            print(e)
        else:
            try:
                movein_date = formatDate(date_str)
            except Exception as e:
                print(e)
            else:
                print(movein_date)
                print("获取到了正确的、格式化后的AvailableFrom，循环结束")
                print("最终的住我家网URL和AvailableFrom", homadorma_url, movein_date)
                break

    time.sleep(random.uniform(5, 10))


def login():
    # 登录页。登录使用POST请求，也是同一url，只是是POST请求方式
    login_url = "https://accounts.craigslist.org/login"

    headers = {
        "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": r"https://www.google.com/",
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }

    # 先get请求登录页，以获取cookie等等数据
    session.get(login_url, headers=headers, timeout=10)

    time.sleep(random.uniform(5, 10))

    # 前5个参数都在登录页的hidden类型表单里，应该去提取value值
    # 这里只是自己构建post请求参数
    data = {
        "step": "confirmation",
        "rt": "",
        "rp": "",
        "t": int(time.time()),
        "p": 0,
        "inputEmailHandle": EMAIL,  # 邮箱
        "inputPassword": PSW,  # 密码
    }

    print(data)

    headers = {
        "Referer": "https://accounts.craigslist.org/login",  # 必须加这个请求头，目标网站使用了防盗链
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }

    response = session.post(login_url, headers=headers, data=data, timeout=10)

    response.encoding = "utf-8"

    print("status code of login : ", response.status_code)

    html = response.text

    with open("1000 login.html", "w", encoding="utf-8") as file:
        file.write(html)

    soup = BeautifulSoup(html, "lxml")

    logout_link = soup.find("a", {"href": "https://accounts.craigslist.org/logout"})

    # 通过查找页面是否有logout链接，检查是否登陆成功
    if logout_link is None:
        print("Failed to login.")
        raise RuntimeError("Failed to login. End the program")
    else:
        print("Success to login")
    time.sleep(random.uniform(5, 10))


# 一步一步地构建请求参数、发送请求，进行租房信息发布
def main():
    global homadorma_url, movein_date

    headers = {
        "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": r"https://accounts.craigslist.org/login/home",
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }
    session.get("https://toronto.craigslist.org/", headers=headers, timeout=6)

    time.sleep(random.uniform(2, 5))

    response = session.get("https://post.craigslist.org/c/tor", headers=headers, timeout=6)
    response.encoding = "utf-8"

    # 一、进入到了 选择 city of toronto 单选框的页面
    print("#### 1 Enter <city of toronto> Page ####")

    html1 = response.text

    with open("1001 city of toronto.html", "w", encoding="utf-8") as file:
        file.write(html1)

    soup = BeautifulSoup(html1, "lxml")

    cryptedStepCheck_input = soup.find("input", {"name": "cryptedStepCheck"})

    data = {
        'n': 1,
        'cryptedStepCheck': cryptedStepCheck_input['value']
    }
    print(data)

    # 提取表单的 url
    form1 = soup.find("form", {"class": "picker"})

    headers = {
        "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": r"https://post.craigslist.org/c/tor",
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }
    time.sleep(random.uniform(5, 10))

    response = session.post(form1['action'], headers=headers, data=data)
    response.encoding = "utf-8"

    # 二、进入了 housing offered 页面
    print("#### 2 enter <housing offered> Page ####")

    html2 = response.text

    with open("1002 housing offered.html", "w", encoding="utf-8") as file:
        file.write(html2)

    soup = BeautifulSoup(html2, "lxml")

    cryptedStepCheck_input = soup.find("input", {"name": "cryptedStepCheck"})

    data = {
        'id': "ho",
        'cryptedStepCheck': cryptedStepCheck_input['value']
    }
    headers = {
        "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": form1['action'],
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }
    print(data)

    # 提取表单的 url
    # form2 = soup.find("form", {"class": "picker"})
    form2 = soup.find("form")

    response = session.post(form2['action'], headers=headers, data=data)

    response.encoding = "utf-8"

    # ##########################################
    # 三、进入了 勾选 rooms & shares 的页面
    print("#### 3 Enter <rooms & shares> Page ####")

    html3 = response.text

    with open("1003 rooms & shares.html", "w", encoding="utf-8") as file:
        file.write(html3)

    soup = BeautifulSoup(html3, "lxml")

    cryptedStepCheck_input = soup.find("input", {"name": "cryptedStepCheck"})

    data = {
        'id': "18",
        'cryptedStepCheck': cryptedStepCheck_input['value'],
        "id2": "1175x835X1175x330X800x600"
    }
    print(data)
    headers = {
        "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": form2['action'],
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }

    # 提取表单的 url
    # form3 = soup.find("form", {"class": "picker"})
    form3 = soup.find("form")

    time.sleep(random.uniform(5, 10))
    response = session.post(form3['action'], headers=headers, data=data)

    response.encoding = "utf-8"

    # 四、进入到了表单页面
    print("#### 4 Enter <Form> Page ####")

    html4 = response.text

    with open("1004 Form.html", "w", encoding="utf-8") as file:
        file.write(html4)

    soup = BeautifulSoup(html4, "lxml")

    cryptedStepCheck_input = soup.find("input", {"name": "cryptedStepCheck"})
    # 提取表单的 url
    # form = soup.find("form", {"id": "postingForm"})
    form4 = soup.find("form")

    # 调用前面定义的获取 已经格式化的Available From（由March 14, 2020 这种格式转成 2020-03-14格式）
    getFormatedgetAvailableFrom()

    data = {
        "PostingTitle": "Toronte student homestay",
        "GeographicArea": "Toronte",
        "postal": r"M2J0B3",
        "PostingBody": r"Please check out this homestay." + homadorma_url,
        "price": "",
        "Sqft": "0",
        "private_room": "1",
        "private_bath": "0",
        "housing_type": "1",
        "laundry": "",
        "parking": "",
        "movein_date": movein_date,
        "FromEMail": "chushiyan@163.com",
        "Privacy": "A",
        "go": "continue",
        "cryptedStepCheck": cryptedStepCheck_input['value'],
    }
    print(data)
    headers = {
        "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": form3['action'],
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }

    time.sleep(random.uniform(5, 10))
    response = session.post(form4['action'], headers=headers, data=data)
    response.encoding = "utf-8"

    # 五、进入了 地图页面
    print("#### 5 Enter the <Google Map> Page ####")
    time.sleep(random.uniform(2, 3))
    html5 = response.text

    with open("1005 Google Map.html", "w", encoding="utf-8") as file:
        file.write(html5)

    soup = BeautifulSoup(html5, "lxml")

    # 提取表单的 url
    form5 = soup.find("form", {"id": "leafletForm"})

    data = {
        "xstreet0": soup.find("input", {"name": "xstreet0"})["value"],
        "xstreet1": soup.find("input", {"name": "xstreet1"})["value"],
        "city": soup.find("input", {"name": "city"})["value"],
        "postal": soup.find("input", {"name": "postal"})["value"],
        "lat": soup.find("input", {"name": "lat"})["value"],
        "lng": soup.find("input", {"name": "lng"})["value"],
        "AreaID": soup.find("input", {"name": "AreaID"})["value"],
        "draggedpin": soup.find("input", {"name": "draggedpin"})["value"],
        "geocoder_latitude": soup.find("input", {"name": "geocoder_latitude"})["value"],
        "geocoder_longitude": soup.find("input", {"name": "geocoder_longitude"})["value"],
        "geocoder_accuracy": soup.find("input", {"name": "geocoder_accuracy"})["value"],
        "cryptedStepCheck": soup.find("input", {"name": "cryptedStepCheck"})["value"],
    }
    print(data)

    headers = {
        "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": form4['action'],
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }

    time.sleep(random.uniform(5, 10))
    response = session.post(form5['action'], headers=headers, data=data)
    response.encoding = "utf-8"

    # 六、进入了 添加图片页面
    print("#### 6 Enter the <Add Image> Page")

    html6 = response.text

    with open("1006 Add Image.html", "w", encoding="utf-8") as file:
        file.write(html6)

    soup = BeautifulSoup(html6, "lxml")

    files = {'file': open('14.jpg', 'rb')}

    data = {
        "cryptedStepCheck": soup.find("input", {"name": "cryptedStepCheck"})["value"],
        "a": "fin",
        "go": "Done with Images"
    }
    print(data)

    headers = {
        "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": form5['action'],
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }

    form6 = soup.find("form", {"class": "add"})
    time.sleep(random.uniform(5, 10))
    response = session.post(form6['action'], headers=headers, data=data, files=files)

    response.encoding = "utf-8"

    html7 = response.text

    with open("1007 The Last page.html", "w", encoding="utf-8") as file:
        file.write(html7)


if __name__ == "__main__":
    # 登录
    login()

    # 执行发布
    main()
