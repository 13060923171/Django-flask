import numpy as np
import pandas as pd
import re
import paddlehub as hub
import jieba


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

    if len(word_num_selected) != 0:
        return ' '.join(word_num_selected)
    else:
        return np.NAN

df['内容'] = df['内容'].apply(emjio_tihuan)
df = df.dropna(subset=['内容'], axis=0)
df['分词'] = df['内容'].apply(get_cut_words)
df['分词'] = df['分词'].replace(' ',np.NAN).replace('\n',np.NAN)
df = df.dropna(how='any', axis=0)
senta = hub.Module(name="senta_bilstm")
texts = df['分词'].tolist()
input_data = {'text': texts}
res = senta.sentiment_classify(data=input_data)
df['情感分值'] = [x['positive_probs'] for x in res]
df = df.dropna(how='any', axis=0)

def main(x):
    x1 = float(x)
    if x1 >= 0.35:
        return 'pos'
    else:
        return 'neg'

df['情感类型'] = df['情感分值'].apply(main)
df.to_csv('./data/情感标签.csv', encoding='utf-8-sig', index=False)