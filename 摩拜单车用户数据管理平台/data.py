#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


class SourceDataDemo:
    @property
    def echart1(self):
        df = pd.read_csv('./data/new_data.csv')
        def main1(x):
            x1 = float(x)
            if x1 <= 1:
                return '1公里以内'
            elif 1 < x1 <= 2:
                return '1公里-2公里'
            elif 2 < x1 <= 3:
                return '2公里-3公里'
            elif 3 < x1 <= 4:
                return '3公里-4公里'
            elif 4 < x1 <= 5:
                return '4公里-5公里'
            else:
                return "5公里以上"

        df['distance(单位:km)'] = df['distance(单位:km)'].apply(main1)
        new_df = df['distance(单位:km)'].value_counts()

        x_data = [x for x in new_df.index]
        y_data = [y for y in new_df.values]

        echart = []
        for x,y in zip(x_data,y_data):
            d = {
                'value':y,'name':x
            }
            echart.append(d)

        return echart

    @property
    def echart2(self):
        df = pd.read_csv('./data/new_data.csv')
        def main1(x):
            x1 = str(x).split(" ")
            x1 = x1[-1]
            x2 = str(x1).split(":")
            x2 = x2[1]
            if int(x2) < 10:
                return '骑行时间少于10分钟'
            elif 10 <= int(x2) <= 30:
                return '骑行时间10-30分钟以内'
            else:
                return '骑行时间大于30分钟'

        df['sum_time'] = df['sum_time'].apply(main1)
        new_df = df['sum_time'].value_counts()

        x_data = [x for x in new_df.index]
        y_data = [y for y in new_df.values]
        echart = []
        for x, y in zip(x_data, y_data):
            d = {
                'value': y, 'name': x
            }
            echart.append(d)

        return echart


    @property
    def echart3(self):
        df = pd.read_csv('./data/new_data.csv')
        df['频次'] = 1
        new_df = df.groupby('week').agg('sum')
        x_data = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六']
        y_data = [y for y in new_df['频次']]

        echart = {
            'xAxis': x_data,
            'data': y_data,
        }
        return echart


    @property
    def echart4(self):
        df = pd.read_csv('./data/new_data.csv')
        df['频次'] = 1
        new_df = df.groupby('hour').agg('sum')
        x_data = [x for x in new_df.index]
        y_data = [y for y in new_df['频次']]

        echart = {
            'xAxis': x_data,
            'data': y_data,
        }
        return echart

    @property
    def echart5(self):
        df = pd.read_csv('./data/轮廓系数.csv')
        x_data = [x for x in df['簇类']]
        y_data = [x for x in df['轮廓系数']]

        echart = {
            'xAxis': x_data,
            'data': y_data,
        }
        return echart

    @property
    def echart6(self):
        df = pd.read_csv('./data/聚类结果.csv')
        new_df = df['聚类结果'].value_counts()
        new_df = new_df.sort_values(ascending=False)
        x_data = ['聚类-{}'.format(x) for x in new_df.index]
        y_data = [y for y in new_df.values]
        echart = []
        for x, y in zip(x_data, y_data):
            d = {
                'value': y, 'name': x
            }
            echart.append(d)
        return echart

    @property
    def echart7(self):
        df = pd.read_csv('./data/new_data.csv')
        new_df = df.groupby('userid').agg('sum')
        new_df = new_df.sort_values(by=['distance(单位:km)'],ascending=False)

        new_df1 = new_df.iloc[:20]
        x_data = ['用户-{}'.format(x) for x in new_df1.index]
        y_data = [round(y,3) for y in new_df1['distance(单位:km)']]

        echart = {
            'xAxis': x_data,
            'data': y_data,
        }
        return echart




class SourceData(SourceDataDemo):
    def __init__(self):
        """
        按照 SourceDataDemo 的格式覆盖数据即可
        """
        super().__init__()
        self.title = '摩拜数据管理平台'
        self.title1 = '骑行公里占比'
        self.title2 = '骑行时间占比'
        self.title3 = '工作日与假日使用量走势'
        self.title4 = '早晚高峰使用量趋势变化'
        self.title5 = '轮廓系数'
        self.title6 = '聚类结果占比'
        self.title7 = '数据聚合分布展示'
        self.title8 = '关联数据展示'
        self.title9 = 'TOP20 用户骑行最高公里数'


if __name__ == '__main__':
    data = SourceDataDemo()
    print(data.echart7)

