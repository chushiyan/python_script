# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time, random

from selenium.webdriver.common.action_chains import ActionChains


def main():
    # 创建一个参数对象，用来控制谷歌浏览器以无界面模式打开
    chrome_options = Options()

    # 如果想开启无界面浏览器（就是看不到浏览器被打开了，浏览器默默执行），就打开下面的注释
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_options=chrome_options)

    # 设置超时20秒
    wait = WebDriverWait(driver, 20)

    # 一、登录移动端微博
    # 打开移动端微博登录页面
    driver.get("https://passport.weibo.cn/signin/login")

    try:
        # 获取用户名输入框
        # name_input = wait.until(expected_conditions.presence_of_element_located((By.ID, "loginName")))
        # print("获取到用户名输入框：")
        # print(name_input)

        # 获取密码输入框
        # password_input = wait.until(expected_conditions.presence_of_element_located((By.ID, 'loginPassword')))
        # print("获取到密码输入框：")
        # print(password_input)

        # 获取登录按钮
        login_btn = wait.until(expected_conditions.presence_of_element_located((By.ID, 'loginAction')))
        print("获取到登录按钮：")
        print(login_btn)

    except Exception as e:
        print(e)
        raise RuntimeError("获取登录按钮失败，程序结束")

    try:
        # 通过让谷歌浏览器执行javascript代码，向用户名输入框、密码输入框设置自己微博的用户名、密码
        # 第一条javascript代码：获取用户名输入框，设置它的value属性值为自己微博的用户名
        # 第二条javascript代码：获取密码输入框，设置它的value属性值为自己微博的密码
        js = '''
        document.getElementById("loginName").setAttribute("value","换成你的微博用户名")
        document.getElementById("loginPassword").setAttribute("value","换成你的微博密码")
        '''

        # 让谷歌浏览执行javascript代码
        driver.execute_script(js)

        print("输入了用户名密码")

        # 睡眠5到8之间的随机浮点数
        time.sleep(random.uniform(5, 8))

        try:
            # 获取鼠标点击链对象
            action = ActionChains(driver)
            # 点击登录按钮
            action.click(login_btn).perform()
            print("点击了登录按钮")

        except Exception as e:
            print(e)
            print("点击登录按钮失败")
            raise RuntimeError("点击登录按钮失败")
    except Exception as e:
        print(e)

    # 随机睡眠10-12之间的浮点数，以便浏览器完成登录
    time.sleep(random.uniform(10, 12))

    # 二、登录成功之后，超话签到
    try:
        # 这里直接指定 朱亚文超话 url
        # 注意：要想签到，得先关注这个超话。
        url = r"https://weibo.com/p/1008084daa7623b0ccb0fba2207c41de75319a/super_index"
        driver.get(url)


        # 获取签到按钮
        sign_btn = wait.until(expected_conditions.presence_of_element_located(
            (By.XPATH, '//div[@class="btn_bed W_fl"]//a[@class="W_btn_b btn_32px"]')))
        print("获取到签到按钮：")
        print(sign_btn)

    except Exception as e:
        print("获取到签到按钮失败")
        print(e)
        raise RuntimeError("获取到签到按钮失败，程序结束")

    try:
        time.sleep(random.uniform(5, 8))

        # 两种方式点击签到：
        # 方式一：
        # 获取鼠标点击链对象
        # action = ActionChains(driver)
        # 点击登录按钮
        # action.click(sign_btn).perform()

        # 方式二：
        sign_btn.click()

        print("点击了签到按钮")

    except Exception as e:
        print(e)
        raise RuntimeError("点击签到按钮失败，程序结束")


    finally:
        time.sleep(100)
        driver.close()


if __name__ == '__main__':

    main()
