#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import re
import jieba
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import roc_curve,auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


class SourceDataDemo:
    @property
    def echart2(self):
        df1 = pd.read_excel('./data/data1.xlsx')
        df2 = pd.read_excel('./data/data2.xlsx')
        df = list(df1['fenci']) + list(df2['fenci'])
        dic = {}
        for d in df:
            d = str(d).split(" ")
            for i in d:
                dic[i] = dic.get(i,0)+1
        ls = list(dic.items())
        ls.sort(key=lambda x:x[1],reverse=True)
        ls = ls[:100]
        data = []
        for key, values in ls:
            di = {"name": '{}-{}'.format(key,values), "value": int(values)}
            data.append(di)
        echart = {
            'data': data,
        }
        return echart

    @property
    def echart3(self):
        df = pd.read_excel('./data/tf_idf_data.xlsx')
        x_data = list(df['word'])[:30]
        y_data = list(df['tfidf'])[:30]
        x_data.reverse()
        y_data.reverse()
        echart = {
            'xAxis': x_data,
            'data': y_data,
        }
        return echart

    @property
    def echart4(self):
        df1 = pd.read_excel('./data/data1.xlsx')
        new_df1 = df1['emotion_type'].value_counts()
        new_df1 = new_df1.sort_index()

        df2 = pd.read_excel('./data/data2.xlsx')
        new_df2 = df2['emotion_type'].value_counts()
        new_df2 = new_df2.sort_index()

        new_df = new_df1.add(new_df2)

        x_data = [x for x in new_df.index]
        y_data = [y for y in new_df.values]
        data = []
        for x,y in zip(x_data,y_data):
            dic = {
                'value':y,'name':x
            }
            data.append(dic)
        return data

    @property
    def echart5(self):
        data = pd.read_csv('./data/score.csv')
        echart = {
            'xAxis1': list(data['准确率']),
            'data1': list(data['准确率_score']),
            'xAxis2': list(data['精确率']),
            'data2': list(data['精确率_score']),
            'xAxis3': list(data['召回率']),
            'data3': list(data['召回率_score']),
            'xAxis4': list(data['F1值']),
            'data4': list(data['F1值_score']),
        }
        return echart


class SourceData(SourceDataDemo):
    def __init__(self):
        """
        按照 SourceDataDemo 的格式覆盖数据即可
        """
        super().__init__()
        self.title = '高校评论舆情洞察系统'
        self.title2 = '高频-词云图'
        self.title3 = 'TF-IDF top30词汇排序'
        self.title4 = '情感占比分布状况'
        self.title5 = '多模型准确率比较'
        self.title6 = '多模型精确率比较'
        self.title7 = '多模型召回率比较'
        self.title8 = '多模型F1值比较'



