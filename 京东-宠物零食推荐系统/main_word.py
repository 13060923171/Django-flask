import jieba
import pandas as pd
import sqlalchemy
import re
import numpy as np
engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/jd')


def hot_word(engine):
    df = pd.read_sql_table('jdsq', engine).loc[:, ['price', 'comment', 'goodrate', 'poorrate', 'attribute']]
    df = df.drop_duplicates(keep='first')

    def title(x):
        if x is not None:
            x = x.split(',')
            x = x[0]
            return x
    df['title'] = df['attribute'].astype(str)
    df['title'] = df['title'].apply(title)

    # 定义分词函数
    def get_cut_words(content_series):
        # 读入停用词表
        stop_words = []

        with open("stopwords_cn.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                stop_words.append(line.strip())
        list_word = []
        # 分词
        word_num = jieba.lcut(content_series.str.cat(sep='。'), cut_all=False)

        # 条件筛选
        word_num_selected = [i for i in word_num if i not in stop_words and len(i) >= 2]
        return word_num_selected

    def is_all_chinese(strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    text1 = get_cut_words(content_series=df['title'])
    ditc = {}
    list_word = []
    list_count = []
    for t in text1:
        ditc[t] = ditc.get(t, 0) + 1
    ls = list(ditc.items())
    ls.sort(key=lambda x: x[1], reverse=True)
    for i in range(len(ls)):
        word, count = ls[i]
        if is_all_chinese(word) == True:
            list_word.append(word)
            list_count.append(count)
    return list_word


# def word_1():
#     list_word = hot_word(df)
#     return list_word


def brand_word(engine):
    df = pd.read_sql_table('jdsq', engine).loc[:, ['goodrate', 'attribute']]
    df = df.replace('', np.nan)
    df = df.dropna(how='any')
    df = df.drop_duplicates(keep='first')

    def title(x):
        if x is not None:
            x = x.split(',')
            x = x[0]
            return x
    df['title'] = df['attribute'].astype(str)
    df['title'] = df['title'].apply(title)


    def brand(x):
        def read_brand(x):
            with open('品牌.txt', 'r', encoding='utf-8')as f:
                content = f.readlines()
            for c in content:
                c = c.strip('\n')
                if c in x:
                    return c
        x = read_brand(x)
        return x

    df['title'] = df['title'].apply(brand)
    df['goodrate'] = df['goodrate'].astype(float)

    df1 = df['title'].value_counts()
    data_pair = [(j, int(k)) for j, k in zip(df1.index,  df1.values)]
    data_pair.sort(key=lambda x: x[1], reverse=True)

    sum_100 = []
    sum_200 = []
    sum_300 = []
    sum_400 = []
    sum_500 = []

    for p,c in zip(df['title'],df['goodrate']):
        if p == data_pair[0][0]:
            sum_100.append(float(c))
        elif p == data_pair[1][0]:
            sum_200.append(float(c))
        elif p == data_pair[2][0]:
            sum_300.append(float(c))
        elif p == data_pair[3][0]:
            sum_400.append(float(c))
        elif p == data_pair[4][0]:
            sum_500.append(float(c))

    sum_100 = np.array(sum_100)
    sum_100 = np.mean(sum_100)

    sum_200 = np.array(sum_200)
    sum_200 = np.mean(sum_200)

    sum_300 = np.array(sum_300)
    sum_300 = np.mean(sum_300)

    sum_400 = np.array(sum_400)
    sum_400 = np.mean(sum_400)

    sum_500 = np.array(sum_500)
    sum_500 = np.mean(sum_500)

    x_data = [data_pair[0][0],data_pair[1][0],data_pair[2][0],data_pair[3][0],data_pair[4][0]]
    y_data = [sum_100,sum_200,sum_300,sum_400,sum_500]

    data_pair1 = [(j, float(k)) for j, k in zip(x_data, y_data)]
    data_pair1.sort(key=lambda x: x[1], reverse=True)

    return data_pair1[0][0]


# def brand_word2():
#     brand = brand_word(df)
#     return brand

