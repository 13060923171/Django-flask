#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
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
    def echart1(self):
        df = pd.read_csv('./data/郑州大学.csv', parse_dates=['时间'], index_col="时间")
        df['发帖数量'] = 1
        new_df1 = df['发帖数量'].resample('W').sum()
        x_data = []
        y_data = []
        for x, y in zip(new_df1.index, new_df1.values):
            x = str(x).split(" ")
            x = x[0]
            if '2023' in str(x):
                x_data.append(x)
                y_data.append(y)
        echart = {
            'xAxis': x_data,
            'series': y_data
        }
        return echart

    @property
    def echart2(self):
        df = pd.read_csv('./data/郑州大学.csv')
        df = df.dropna(how='any',axis=0)
        def emjio_tihuan(x):
            x1 = str(x)
            x2 = re.sub('(\[.*?\])', "", x1)
            x3 = re.sub(r'@[\w\u2E80-\u9FFF]+:?|\[\w+\]', '', x2)
            x4 = re.sub(r'\n', '', x3)
            return x4

        def is_all_chinese(strs):
            for _char in strs:
                if not '\u4e00' <= _char <= '\u9fa5':
                    return False
            return True

        stop_words = []
        with open("./data/stopwords_cn.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                stop_words.append(line.strip())

        def get_cut_words(content_series):
            # 读入停用词表
            # 分词
            word_num = jieba.lcut(content_series, cut_all=False)

            # 条件筛选
            word_num_selected = [i for i in word_num if i not in stop_words and len(i) >= 2 and is_all_chinese(i) == True]

            return ' '.join(word_num_selected)

        df['内容'] = df['内容'].apply(emjio_tihuan)
        df = df.dropna(subset=['内容'], axis=0)
        df['内容'] = df['内容'].apply(get_cut_words)
        dic = {}
        for d in df['内容']:
            d = str(d).split(" ")
            for i in d:
                dic[i] = dic.get(i,0)+1
        ls = list(dic.items())
        ls.sort(key=lambda x:x[1],reverse=True)
        ls = ls[1:101]
        data = []
        for key, values in ls:
            di = {"name": key, "value": values}
            data.append(di)

        echart = {
            'data': data,
        }
        return echart

    @property
    def echart3(self):
        df = pd.read_csv('./data/郑州大学.csv')
        df = df.dropna(how='any', axis=0)

        def emjio_tihuan(x):
            x1 = str(x)
            x2 = re.sub('(\[.*?\])', "", x1)
            x3 = re.sub(r'@[\w\u2E80-\u9FFF]+:?|\[\w+\]', '', x2)
            x4 = re.sub(r'\n', '', x3)
            return x4

        def is_all_chinese(strs):
            for _char in strs:
                if not '\u4e00' <= _char <= '\u9fa5':
                    return False
            return True

        stop_words = []
        with open("./data/stopwords_cn.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                stop_words.append(line.strip())

        df['内容'] = df['内容'].apply(emjio_tihuan)
        df = df.dropna(subset=['内容'], axis=0)

        f = open('./data/fenci.txt', 'w', encoding='utf-8-sig')
        for line in df['内容']:
            line = line.strip('\n')
            # 停用词过滤
            seg_list = jieba.cut(line, cut_all=False)
            cut_words = (" ".join(seg_list))

            # 计算关键词
            all_words = cut_words.split()
            c = Counter()
            for x in all_words:
                if len(x) >= 2 and x != '\r\n' and x != '\n':
                    if is_all_chinese(x) == True and x not in stop_words:
                        c[x] += 1
            output = ""
            for (k, v) in c.most_common():
                output += k + " "

            f.write(output + "\n")
        else:
            f.close()

        corpus = []
        # 读取预料 一行预料为一个文档
        for line in open('./data/fenci.txt', 'r', encoding='utf-8').readlines():
            corpus.append(line.strip('\n'))

            # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
        vectorizer = CountVectorizer()

        # 该类会统计每个词语的tf-idf权值
        transformer = TfidfTransformer()

        # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
        tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
        # 获取词袋模型中的所有词语
        word = vectorizer.get_feature_names_out()

        # 将tf-idf矩阵抽取出来 元素w[i][j]表示j词在i类文本中的tf-idf权重
        weight = tfidf.toarray()

        data = {'word': word,
                'tfidf': weight.sum(axis=0).tolist()}
        df2 = pd.DataFrame(data)
        df2['tfidf'] = df2['tfidf'].astype('float64')
        df2 = df2.sort_values(by=['tfidf'], ascending=False)

        x_data = list(df2['word'])[:30]
        y_data = list(df2['tfidf'])[:30]
        x_data.reverse()
        y_data.reverse()
        echart = {
            'xAxis': x_data,
            'data': y_data,
        }
        return echart


    @property
    def echart4(self):
        df = pd.read_csv('./data/情感标签.csv')
        new_df = df['情感类型'].value_counts()
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
        self.title1 = '周发帖数量趋势'
        self.title2 = '高频-词云图'
        self.title3 = 'TF-IDF top30词汇排序'
        self.title4 = '情感占比分布状况'
        self.title5 = '多模型准确率比较'
        self.title6 = '多模型精确率比较'
        self.title7 = '多模型召回率比较'
        self.title8 = '多模型F1值比较'
        self.title9 = '多模型ROC曲线比较'



