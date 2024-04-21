import pandas as pd

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

df1 = pd.read_excel('../data/data1.xlsx')
df2 = pd.read_excel('../data/data2.xlsx')
df = list(df1['fenci']) + list(df2['fenci'])

corpus = []
# 读取预料 一行预料为一个文档
for line in df:
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
df2.to_excel('../data/tf_idf_data.xlsx', index=False)