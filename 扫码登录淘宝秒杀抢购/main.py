# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 淘宝秒杀脚本，扫码登录版
from selenium import webdriver
import datetime
import time, random


def login():
    # 打开淘宝登录页，并进行扫码登录
    browser.get("https://www.taobao.com")
    time.sleep(random.uniform(5, 8))
    if browser.find_element_by_link_text("亲，请登录"):
        browser.find_element_by_link_text("亲，请登录").click()
        print("请在15秒内完成扫码")
        time.sleep(random.uniform(15, 20))
        # 进入购物车
        browser.get("https://cart.taobao.com/cart.htm")

    time.sleep(random.uniform(3, 5))

    now = datetime.datetime.now()
    print('login success:', now.strftime('%Y-%m-%d %H:%M:%S'))


def buy(times, choose):
    # if choose == 2:
    #     print("请手动勾选需要购买的商品")

    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # 对比时间，时间到的话就点击结算
        if now > times:

            # 进入购物车
            browser.get("https://cart.taobao.com/cart.htm")

            # 点击购物车里全选按钮
            # if choose == 1:
            while True:
                try:
                    if browser.find_element_by_id("J_SelectAll1"):
                        browser.find_element_by_id("J_SelectAll1").click()
                        break
                except Exception as e:
                    print("找不到全选复选框：")
                    print(e)

            # 点击结算按钮
            while True:
                try:
                    if browser.find_element_by_link_text("结 算"):
                        browser.find_element_by_link_text("结 算").click()
                        print("结算成功")
                        break
                except Exception as e:
                    print("结算失败：")
                    print(e)

            while True:
                try:
                    if browser.find_element_by_link_text('提交订单'):
                        browser.find_element_by_link_text('提交订单').click()
                        now1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                        print("抢购成功时间：%s" % now1)
                except Exception as e:
                    print("提交订单失败：")
                    print(e)

            time.sleep(0.005)


if __name__ == "__main__":
    # times = input("请输入抢购时间，格式如(2018-09-06 11:20:00.000000):")
    times = '2020-01-02 14:00:00.000000'
    # times = '2020-01-05 21:35:00.000000'

    browser = webdriver.Chrome()
    login()

    # choose = int(input("到时间自动勾选购物车请输入“1”，否则输入“2”："))

    choose = 1
    buy(times, choose)
