#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import sqlalchemy
from main_bar import price_bar
from main_pie import brand_pie
from main_map import production_map
from main_bar1 import comment_bar
from main_pie2 import goodrate_pie
from main_bar2 import taste_bar
from main_line import price_line


engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/jd')


data1, data2, data3, data4, data5, data6 = price_bar(engine)
sum_100, sum_200, sum_300, sum_400, sum_500, sum_600 = comment_bar(engine)
data_pair_1 = brand_pie(engine)
domestic,domestic_2,import1,import_2 = goodrate_pie(engine)
map_data = production_map(engine)
test_y, y_pred, x_data, score, test_x = price_line(engine)
taste1, taste2, taste3, taste4, taste5, taste6, taste7, taste8 = taste_bar(engine)

class SourceDataDemo:
    def __init__(self):
        self.title = '宠物零食市场分析系统'

        self.echart1_data = {
            'title': '零食价格区间分布',
            'data': [
                {"name": "100及以下", "value": data1},
                {"name": "100-200元", "value": data2},
                {"name": "200-300元", "value": data3},
                {"name": "300-400元", "value": data4},
                {"name": "400-500元", "value": data5},
                {"name": "500及以上", "value": data6},
            ]
        }

        self.echart2_data = {
            'title': '价格与销量对比',
            'data': [
                {"name": "100及以下", "value": sum_100},
                {"name": "100-200元", "value": sum_200},
                {"name": "200-300元", "value": sum_300},
                {"name": "300-400元", "value": sum_400},
                {"name": "400-500元", "value": sum_500},
                {"name": "500及以上", "value": sum_600},
            ]
        }


        self.echarts3_data = {
            'title': '国产/进口 占比情况',
            'data': [
                {"name": data_pair_1[0][0], "value": data_pair_1[0][1]},
                {"name": data_pair_1[1][0], "value": data_pair_1[1][1]},
            ]
        }

        self.echart4_data = {
            'title': '价格预测',
            'data': [
                {"name": "样本价格", "value": test_y[0:70]},
                {"name": "预测价格", "value": y_pred[0:70]},
            ],
            'xAxis': x_data[0:70],
        }

        self.echart5_data = {
            'title': '口味热爱程度',
            'data': [
                {"name": "混合口味", "value": taste1},
                {"name": "牛肉味", "value": taste2},
                {"name": "鸡肉味", "value": taste3},
                {"name": "鸭肉味", "value": taste4},
                {"name": "奶香味", "value": taste5},
                {"name": "鱼肉味", "value": taste6},
                {"name": "羊肉味", "value": taste7},
                {"name": "水果味", "value": taste8},
            ]
        }


        self.echart6_data = {
            'title': '国产/进口 平均好评对比',
            'data': [
                {"name": "国产", "value": domestic, "value2": domestic_2, "color": "01", "radius": ['59%', '70%']},
                {"name": "进口", "value": import1, "value2": import_2, "color": "02", "radius": ['49%', '60%']},
            ]
        }

        self.map_1_data = {
            'symbolSize': 1,
            'data': map_data
        }

    @property
    def echart1(self):
        data = self.echart1_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')]
        }
        return echart

    @property
    def echart2(self):
        data = self.echart2_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')]
        }
        return echart

    @property
    def echart3(self):
        data = self.echarts3_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart



    @property
    def echart4(self):
        data = self.echart4_data
        echart = {
            'title': data.get('title'),
            'names': [i.get("name") for i in data.get('data')],
            'xAxis': data.get('xAxis'),
            'data': data.get('data'),
        }
        return echart

    @property
    def echart5(self):
        data = self.echart5_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echart6(self):
        data = self.echart6_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def map_1(self):
        data = self.map_1_data
        echart = {
            'symbolSize': data.get('symbolSize'),
            'data': data.get('data'),
        }
        return echart


class SourceData(SourceDataDemo):

    def __init__(self):
        """
        按照 SourceDataDemo 的格式覆盖数据即可
        """
        super().__init__()
        self.title = '宠物零食市场分析系统'
