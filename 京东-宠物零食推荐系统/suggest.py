#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sqlalchemy
from main_bar import price_bar
from main_pie import brand_pie
from main_map import production_map
from main_bar1 import comment_bar,price_good
from main_pie2 import goodrate_pie
from main_bar2 import taste_bar,taste_good
from main_line import price_line
from main_word import hot_word,brand_word

engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/jd')


def comment_bar1(engine):
    sum_100, sum_200, sum_300, sum_400, sum_500, sum_600 = comment_bar(engine)
    y_data = [sum_100, sum_200, sum_300, sum_400, sum_500, sum_600]
    x_data = ['100及以下','100-200元','200-300元','300-400元','400-500元','500及以上']
    data_pair = [(j,int(k)) for j,k in zip(x_data,y_data)]
    data_pair.sort(key=lambda x:x[1],reverse=True)
    return data_pair[0][0],data_pair[1][0]


def taste_bar1(engine):
    taste1, taste2, taste3, taste4, taste5, taste6, taste7, taste8 = taste_bar(engine)
    y_data = [taste1, taste2, taste3, taste4, taste5, taste6, taste7, taste8]
    x_data = ['混合口味','牛肉味','鸡肉味','鸭肉味','奶香味','鱼肉味','羊肉味','水果味']
    data_pair = [(j, int(k)) for j, k in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1], reverse=True)
    return data_pair[0][0],data_pair[1][0],data_pair[2][0]


def merchant():
    price1, price2 = comment_bar1(engine)
    brand = brand_pie(engine)
    brand.sort(key=lambda x: x[1], reverse=True)
    brand = brand[0][0]
    taste1, taste2, taste3 = taste_bar1(engine)
    str_word = hot_word(engine)
    str_word = '、'.join(str_word[0:10])
    return price1,price2,brand,taste1,taste2,taste3,str_word


def taste_good1(engine):
    taste1,taste2,taste3,taste4,taste5,taste6,taste7,taste8 = taste_good(engine)

    y_data = [taste1, taste2, taste3, taste4, taste5, taste6, taste7, taste8]
    x_data = ['混合口味', '牛肉味', '鸡肉味', '鸭肉味', '奶香味', '鱼肉味', '羊肉味', '水果味']
    data_pair = []
    for j, k in zip(x_data, y_data):
        data_pair.append([j, float(k)])
    data_pair.sort(key=lambda x: x[1], reverse=True)
    return data_pair[0][0]


def price_good1(engine):
    sum_100, sum_200, sum_300, sum_400, sum_500, sum_600 = price_good(engine)
    y_data = [sum_100, sum_200, sum_300, sum_400, sum_500, sum_600]
    x_data = ['100及以下', '100-200元', '200-300元', '300-400元', '400-500元', '500及以上']
    data_pair = [(j, float(k)) for j, k in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1], reverse=True)
    return data_pair[0][0]


def brand_good(engine):
    domestic,domestic_2,import1,import_2 = goodrate_pie(engine)
    y_data = [domestic,import1]
    x_data = ['国产','进口']
    data_pair = [(j, float(k)) for j, k in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1], reverse=True)
    return data_pair[0][0]


def buyer():
    taste1 = taste_good1(engine)
    price1 = price_good1(engine)
    brand1 = brand_good(engine)
    word1 = brand_word(engine)
    return taste1,price1,brand1,word1

