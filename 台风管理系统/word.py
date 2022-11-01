import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from pyecharts.globals import ThemeType
import re
import jieba
import jieba.analyse
from collections import Counter

def main(name):
    df = data[data['关键词'] == name]

    def is_all_chinese(strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    def get_cut_words(content_series):
        # 读入停用词表
        stop_words = []
        with open("./demo/data/stopwords_cn.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                stop_words.append(line.strip())

        # 分词
        word_num = jieba.lcut(content_series.str.cat(sep='。'), cut_all=False)

        # 条件筛选
        word_num_selected = [i for i in word_num if i not in stop_words and len(i) >= 2 and is_all_chinese(i) == True]
        return word_num_selected

    text1 = get_cut_words(content_series=df['发布内容'])
    d = {}
    for t in text1:
        d[t] = d.get(t,0) + 1
    ls = list(d.items())
    ls.sort(key=lambda x:x[1],reverse=True)
    ls = ls[0:100]

    c = (
        WordCloud()
            .add("", ls, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
            .set_global_opts(title_opts=opts.TitleOpts(title="{}-词云".format(name)))
            .render("./templates/{}-词云.html".format(name))
    )


if __name__ == '__main__':
    data = pd.read_excel('./demo/data/微博数据.xlsx')
    name_data = data['关键词'].value_counts()
    x_data1 = [n for n in name_data.index]
    for o in x_data1:
        main(o)