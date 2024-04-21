#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import warnings
import re
warnings.filterwarnings('ignore')

df2 = pd.read_excel('./data/data2.xlsx')
df2['发帖数量'] = 1
df2['创建时间'] = pd.to_datetime(df2['创建时间'])
# 设置'创建时间'列为索引，以便使用resample函数
df2.set_index('创建时间', inplace=True)
# 按周重新采样，并统计每周的频次
weekly_counts = df2.resample('W').count()
day3_counts = df2.resample('3d').count()
month_counts = df2.resample('M').count()
name_people = df2['作者'].value_counts()
name_people = name_people.iloc[:20]
name_x_data = [str(x) for x in name_people.index]
name_x_data.reverse()
name_y_data = [int(y) for y in name_people.values]
name_y_data.reverse()

df3 = df2[df2['emotion_type'] == '积极']
positive_month_counts = df3.resample('M').count()
df4 = df2[df2['emotion_type'] == '消极']
negative_month_counts = df4.resample('M').count()

df1 = pd.read_excel('./data/data1.xlsx')

def demo(x):
    data = x
    new_data = data['emotion_type'].value_counts()
    d = {}
    for key, values in zip(new_data.index, new_data.values):
        d[key] = values
    try:
        number_neg = int(d['消极'])
    except:
        number_neg = 0
    return number_neg


post_df1 = df1.groupby('帖子id').apply(demo)
post_df1 = post_df1.sort_values(ascending=False)
post_df1 = post_df1.iloc[:20]
df_result = []
for p in post_df1.index:
    # 根据条件返回符合条件的一行内容
    condition = df2['帖子id'] == p
    if not df2[condition].empty:
        first_row = df2[condition].iloc[0]
        df_result.append(first_row)
df = pd.concat(df_result, axis=0)

str1 = []
for title, conent in zip(df['帖子标题'], df['摘要']):
    str2 = str(title)
    pattern = re.compile(r'[\u4e00-\u9fff]+')  # 匹配中文字符的正则表达式
    matches = pattern.findall(str2)  # 查找所有中文字符
    clean_text = ''.join(matches)  # 将所有找到的中文字符连接成一个新字符串
    str1.append(clean_text)



class SourceDataDemo:
    def __init__(self):
        self.title = '高校评论舆情大屏展示'
        df1 = pd.read_excel('./data/data1.xlsx')
        df2 = pd.read_excel('./data/data2.xlsx')

        self.counter = {'name': '总评论数', 'value': len(df1)}
        self.counter2 = {'name': '总发帖数', 'value':len(df2)}

    @property
    def echart1(self):
        echart = {
            'title': '每三日-发贴趋势分布',
            'xAxis': [str(x).split(" ")[0] for x in day3_counts.index],
            'data': [int(y) for y in day3_counts['发帖数量']],
        }
        return echart

    @property
    def echart2(self):
        echart = {
            'title': '每周-发贴趋势分布',
            'xAxis': [str(x).split(" ")[0] for x in weekly_counts.index],
            'data': [int(y) for y in weekly_counts['发帖数量']],
        }
        return echart

    @property
    def echart3(self):
        echart = {
            'title': '每月-发贴趋势分布',
            'xAxis': [str(x).split(" ")[0] for x in month_counts.index],
            'data': [int(y) for y in month_counts['发帖数量']],
        }
        return echart

    @property
    def echart4(self):
        echart = {
            'title': '发帖频率top20的作者',
            'xAxis': name_x_data,
            'data': name_y_data,
        }
        return echart

    @property
    def echart5(self):
        echart = {
            'title': '每月正负面分布趋势',
            'name':['正面','负面'],
            'xAxis': [str(x).split(" ")[0] for x in positive_month_counts.index],
            'data1': [int(y) for y in positive_month_counts['发帖数量']],
            'data2': [int(y) for y in negative_month_counts['发帖数量']],
        }
        return echart

    @property
    def echart6(self):
        echart = {
            'title': '特别需要注意的帖子',
        }
        return echart


class SourceData1(SourceDataDemo):
    def __init__(self):
        """
        按照 SourceDataDemo 的格式覆盖数据即可
        """
        super().__init__()
        self.title = '高校评论舆情大屏展示'
        self.comment = str1


