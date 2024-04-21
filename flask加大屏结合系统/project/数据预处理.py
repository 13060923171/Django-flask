import pandas as pd
import os
from tqdm import tqdm
import numpy as np
import re
import jieba
import jieba.posseg as pseg
from snownlp import SnowNLP

def main1(df):
    # 导入停用词列表
    stop_words = ['北大','复旦','中山大学','中大','清华','交大','复旦大学','北京大学','清华大学','上海交通大学','交通大学']
    with open("../data/stopwords_cn.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            stop_words.append(line.strip())

    # 去掉标点符号，以及机械压缩
    def preprocess_word(word):
        word1 = str(word)
        # word1 = re.sub(r'转发微博', '', word1)
        word1 = re.sub(r'#\w+#', '', word1)
        word1 = re.sub(r'【.*?】', '', word1)
        word1 = re.sub(r'@[\w]+', '', word1)
        word1 = re.sub(r'[a-zA-Z]', '', word1)
        word1 = re.sub(r'\.\d+', '', word1)
        return word1

    def emjio_tihuan(x):
        x1 = str(x)
        x2 = re.sub('(\[.*?\])', "", x1)
        x3 = re.sub(r'@[\w\u2E80-\u9FFF]+:?|\[\w+\]', '', x2)
        x4 = re.sub(r'\n', '', x3)
        return x4

    # 判断是否为中文
    def is_all_chinese(strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    # 定义机械压缩函数
    def yasuo(st):
        for i in range(1, int(len(st) / 2) + 1):
            for j in range(len(st)):
                if st[j:j + i] == st[j + i:j + 2 * i]:
                    k = j + i
                    while st[k:k + i] == st[k + i:k + 2 * i] and k < len(st):
                        k = k + i
                    st = st[:j] + st[k:]
        return st

    def get_cut_words(content_series):
        try:
            # 对文本进行分词和词性标注
            words = pseg.cut(content_series)
            # 保存名词和形容词的列表
            nouns_and_adjs = []
            # 逐一检查每个词语的词性，并将名词和形容词保存到列表中
            for word, flag in words:
                if word not in stop_words and len(word) >= 2 and is_all_chinese(word) == True:
                    # 如果是名词或形容词，就将其保存到列表中
                    nouns_and_adjs.append(word)
            if len(nouns_and_adjs) != 0:
                return ' '.join(nouns_and_adjs)
            else:
                return np.NAN
        except:
            return np.NAN

    def analyze_sentiment(text):
        s = SnowNLP(text)
        sentiment = s.sentiments
        if sentiment >= 0.4:
            return '积极'
        else:
            return '消极'


    df = df.drop_duplicates(subset=['摘要'])
    df['摘要'] = df['摘要'].apply(preprocess_word)
    df['摘要'] = df['摘要'].apply(emjio_tihuan)
    df['摘要'] = df['摘要'].apply(yasuo)
    df.dropna(subset=['摘要'], axis=0, inplace=True)
    df['fenci'] = df['摘要'].apply(get_cut_words)
    new_df = df.dropna(subset=['fenci'], axis=0)
    new_df['emotion_type'] = new_df['fenci'].apply(analyze_sentiment)
    new_df.to_excel('../data/data2.xlsx', index=False)


if __name__ == '__main__':
    df1 = pd.read_excel('../data/post_list.xlsx')
    main1(df1)

