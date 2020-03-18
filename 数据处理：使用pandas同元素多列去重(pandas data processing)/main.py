# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

# 功能：读取excel表格，使用pandas同元素多列去重

# 读取excel，构建成DataFrame对象
df = pd.DataFrame(pd.read_excel("data.xlsx"))

# 构建临时列
# 比如 北京|洛桑
#      洛桑|北京
df['temp'] = df['city_out'] + '|' + df['city_in']

p = []

for i in df['temp'].tolist():

    # 排序
    # 一经排序 北京|洛桑  或者 洛桑|北京  ， 都成了 北京|洛桑 ，这样就能去重
    tmp = sorted(i.split('|')) # The most important part,sort

    p.append(tmp[0] + '|' + tmp[1])

    df['temp'] = pd.Series(p)

# 根据临时列去重
df = df.drop_duplicates('temp')

# 删除临时列
del df['temp']

print(df)

# 将处理后的结果写入新的excel文件中
df.to_excel("result.xlsx", encoding='utf-8', index=False, header=True)