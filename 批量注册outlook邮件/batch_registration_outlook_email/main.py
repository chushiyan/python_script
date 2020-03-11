from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
import time
import random
from names import *
import hashlib
import json
import requests


def regist(account_info, file):
    # 创建一个参数对象，用来控制谷歌浏览器以无界面模式打开
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    response = requests.get('http://dps.kdlapi.com/api/getdps/?orderid=965447514677322&num=1&pt=1&dedup=1&sep=1')

    # chrome_options.add_argument("--proxy-server=http://218.67.39.234:19144")
    chrome_options.add_argument("--proxy-server=http://" + response.text)

    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.set_window_size(1920, 3000)

    # driver.implicitly_wait(20)

    wait = WebDriverWait(driver, 15)

    # 1\
    driver.get(r'https://outlook.live.com/owa/')

    try:
        create_account_link = wait.until(expected_conditions.visibility_of_element_located((By.LINK_TEXT, '创建免费帐户')))
        print(create_account_link)
    except Exception as e:
        print('获取创建免费账号失败......')
        print(e)
        # return
    else:
        create_account_link.click()

    min_second = 4
    max_cecond = 6
    time.sleep(random.random() + random.randint(min_second, max_cecond))

    # #############  1、账户名页面  #############
    # get username input
    try:
        username_input = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="MemberName"]')))
        print(username_input)
    except Exception as e:
        print(e)
        print('get username input failed......')
        # return
    else:
        username_input.send_keys(account_info['username'])

    # get Next input
    try:
        next_input = wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//input[@id="iSignupAction"]')))
        print(next_input)
    except Exception as e:
        print(e)
        print('get Next input failed......')
        # return
    else:
        next_input.click()

    time.sleep(random.random() + random.randint(min_second, max_cecond))
    # #############  2、密码页面  #############
    # get password input
    try:
        password_input = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="PasswordInput"]')))
        print(password_input)
    except Exception as e:
        print(e)
        print('get password input failed......')
        # return
    else:
        password_input.send_keys(account_info['password'])

    # get Next input
    try:
        next_input = wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//input[@id="iSignupAction"]')))
        print(next_input)
    except Exception as e:
        print(e)
        print('get Next input failed......')
        # return
    else:
        next_input.click()

    time.sleep(random.random() + random.randint(min_second, max_cecond))

    # #############  3、姓、名输入页面 #############
    # get LastName input
    try:
        last_name_input = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="LastName"]')))
        print(last_name_input)
    except Exception as e:
        print(e)
        print('get LastName input failed......')
        # return
    else:
        last_name_input.send_keys(account_info['last_name'])

    # get FirstName input
    try:
        first_name_input = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="FirstName"]')))
        print(first_name_input)
    except Exception as e:
        print(e)
        print('get FirstName input failed......')
        # return
    else:
        first_name_input.send_keys(account_info['first_name'])

    # get Next input
    try:
        next_input = wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//input[@id="iSignupAction"]')))
        print(next_input)
    except Exception as e:
        print(e)
        print('get Next input failed......')
        # return
    else:
        next_input.click()

    time.sleep(random.random() + random.randint(min_second, max_cecond))

    # #############  4、国家、出生年月日下拉选框 #############
    try:
        birth_year = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//select[@id="BirthYear"]')))
        print(birth_year)
    except Exception as e:
        print(e)
        print('get birth_year_select failed......')
        # return
    else:
        birth_year_select = Select(birth_year)
        birth_year_select.select_by_value(account_info['birth_year'])

    try:
        birth_month = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//select[@id="BirthMonth"]')))
        print(birth_month)
    except Exception as e:
        print(e)
        print('get birth_month_select failed......')
        # return
    else:
        birth_month_select = Select(birth_month)
        birth_month_select.select_by_index(account_info['birth_month'])

    try:
        birth_day = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//select[@id="BirthDay"]')))
        print(birth_day)
    except Exception as e:
        print(e)
        print('get birth_day_select  failed......')
        # return
    else:
        birth_day_select = Select(birth_day)
        birth_day_select.select_by_index(account_info['birth_day'])

    # get Next input
    try:
        next_input = wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//input[@id="iSignupAction"]')))
        print(next_input)
    except Exception as e:
        print(e)
        print('get Next input failed......')
        # return
    else:
        next_input.click()

    time.sleep(random.random() + random.randint(min_second, max_cecond))

    # #############  5、验证码页面 #############
    try:
        img = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//div[@id="hipTemplateContainer"]//img')))
        print(img)
    except Exception as e:
        print(e)
        print('get code image failed......')
        # return
    else:

        img.screenshot('001.png')

    code = input("请输入验证码：\n")


    try:
        code_input = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//input[@type="text"]')))
        print(img)
    except Exception as e:
        print(e)
        print('get code input failed......')
        # return
    else:
        code_input.send_keys(code)

    time.sleep(random.random() + random.randint(min_second, max_cecond))
    # get Next input
    try:
        next_input = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//input[@id="iSignupAction"]')))
        print(next_input)
    except Exception as e:
        print(e)
        print('get Next input failed......')
        # return
    else:
        next_input.click()

    time.sleep(random.random() + random.randint(min_second, max_cecond))

    # ########## 6、 你好，欢迎使用 Outlook.com页面 ############
    # get Next input
    try:
        next_input = wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/section/div/div/section/button')))
        print(next_input)
    except Exception as e:
        print(e)
        print('get Next input failed......')
        # return
    else:
        next_input.click()

    time.sleep(random.random() + random.randint(min_second, max_cecond))

    # ########## 7、 首先需要设置一些内容 ############

    # get Next input
    try:
        next_input = wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/section/div/div[2]/section/button[2]')))
        print(next_input)
    except Exception as e:
        print(e)
        print('get Next input failed......')
        # return
    else:
        next_input.click()

    time.sleep(random.random() + random.randint(min_second, max_cecond))
    # ########## 8、 设置样式 ############
    # get Next input
    try:
        theme_div = wait.until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//*[@id="theme_table"]/div[{}]'.format(random.randint(1, 40)))))
        print(theme_div)
    except Exception as e:
        print(e)
        print('get Next input failed......')
        # return
    else:
        theme_div.click()

    time.sleep(random.random() + random.randint(min_second, max_cecond))
    # ########## 9、 首先需要设置一些内容 ############

    # get Next input
    try:
        next_input = wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/section/div/div[2]/section/button[2]')))
        print(next_input)
    except Exception as e:
        print(e)
        print('get Next input failed......')
        # return
    else:
        next_input.click()

    time.sleep(random.random() + random.randint(min_second, max_cecond))
    # ########## 10、 添加签名 ############

    # get Next input
    try:
        next_input = wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/section/div/div[2]/section/button[2]')))
        print(next_input)
    except Exception as e:
        print(e)
        print('get Next input failed......')
        # return
    else:
        next_input.click()

    time.sleep(random.random() + random.randint(min_second, max_cecond))
    # ########## 11、 开始使用 ############

    # get Next input
    try:
        next_input = wait.until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '/html/body/section/div/div[2]/section/section/section/div/button')))
        print(next_input)
    except Exception as e:
        print(e)
        print('get Next input failed......')
        # return
    else:
        next_input.click()

    json_line = json.dumps(dict(account_info)) + ",\n"
    file.write(json_line)

    time.sleep(100000)


# create username password birth_year birth_month  birth_day
def create_account_info():
    account_info = {}

    account_info['first_name'] = random.choice(FIRST_NAME)

    account_info['last_name'] = random.choice(LAST_NAME)

    # random_string = hashlib.md5((first_name + "_" + last_name).encode()).hexdigest()

    string_list = random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 10)

    account_info['username'] = account_info['first_name'] + account_info['last_name'] + ''.join(string_list)

    account_info['email'] = account_info['username'] + "@outlook.com"

    account_info['password'] = random_string = hashlib.md5(account_info['username'].encode()).hexdigest()

    account_info['birth_year'] = random.choice(BIRTH_YEAR)

    account_info['birth_month'] = random.choice(BIRTH_MONTH)

    account_info['birth_day'] = random.choice(BIRTH_DAY)

    print(account_info)

    return account_info


if __name__ == '__main__':

    file = open('outlook_emails_.json', 'a+', encoding='utf-8')

    i = 1
    while i < 2:
        account_info = create_account_info()

        regist(account_info, file)

        i += 1
