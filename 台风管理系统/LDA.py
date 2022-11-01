import pandas as pd
import pyLDAvis
import pyLDAvis.gensim
import re
import jieba
import jieba.analyse
from collections import Counter
from gensim import corpora, models, similarities

def main(name):
    df = data[data['关键词'] == name]

    def is_all_chinese(strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    stop_words = []

    with open("./demo/data/stopwords_cn.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            stop_words.append(line.strip())

    f = open('./demo/data/{}-fenci.txt'.format(name), 'w', encoding='utf-8')
    for line in df['发布内容']:
        line = line.strip('\n')
        # 停用词过滤
        line = re.sub('[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "", line)
        seg_list = jieba.cut(line, cut_all=False)
        cut_words = (" ".join(seg_list))
        # 计算关键词
        all_words = cut_words.split()
        c = Counter()
        for x in all_words:
            if len(x) > 1 and x != '\r\n':
                if is_all_chinese(x) == True and x not in stop_words and len(x) >= 2:
                    c[x] += 1
        # Top30
        output = ""
        # print('\n词频统计结果：')
        for (k, v) in c.most_common(30):
            # print("%s:%d"%(k,v))
            output += k + " "

        f.write(output + "\n")
    else:
        f.close()

    fr = open('./demo/data/{}-fenci.txt'.format(name), 'r', encoding='utf-8')
    train = []
    for line in fr.readlines():
        line = [word.strip() for word in line.split(' ') if len(word) >= 2]
        train.append(line)

    dictionary = corpora.Dictionary(train)
    corpus = [dictionary.doc2bow(text) for text in train]

    topic_lda = 3

    lda = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=topic_lda)

    data1 = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.save_html(data1, "./templates/{}-LDA主题模型.html".format(name))


if __name__ == '__main__':
    data = pd.read_excel('./demo/data/微博数据.xlsx')
    name_data = data['关键词'].value_counts()
    x_data1 = [n for n in name_data.index]
    for o in x_data1:
        main(o)