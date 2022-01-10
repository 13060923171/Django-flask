import pandas as pd
import numpy as np
import sqlalchemy
import re
engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/jd')


def taste_bar(engine):
    df = pd.read_sql_table('jdsq', engine).loc[:, ['attribute', 'comment']]
    df = df.replace('', np.nan)
    df = df.dropna(how='any')
    df = df.drop_duplicates(keep='first')

    def taste_bar1(x):
        x1 = re.compile(",(.*?)味,")
        x2 = x1.findall(x)
        if len(x2) > 0:
            x2 = x2[0]
            x2 = str(x2)
            x2 = x2.split(',')
            x2 = x2[-1]
            x2 = str(x2) + '味'
            return x2
        else:
            return None
    df['attribute'] = df['attribute'].astype(str)
    df['attribute'] = df['attribute'].apply(taste_bar1)
    def comment_number1(x):
        x = str(x)
        x = x.replace('+','').replace('万','0000')
        return x
    df['comment'] = df['comment'].astype(str)
    df['comment'] = df['comment'].apply(comment_number1)

    taste1 = 0
    taste2 = 0
    taste3 = 0
    taste4 = 0
    taste5 = 0
    taste6 = 0
    taste7 = 0
    taste8 = 0

    for p,c in zip(df['attribute'],df['comment']):
        if p is not None:
            if '混合口味' in p:
                taste1 += int(c)
            if '牛肉味' in p:
                taste2 += int(c)
            if '鸡肉味' in p:
                taste3 += int(c)
            if '鸭肉味' in p:
                taste4 += int(c)
            if '奶香味' in p:
                taste5 += int(c)
            if '鱼肉味' in p:
                taste6 += int(c)
            if '羊肉味' in p:
                taste7 += int(c)
            if '水果味' in p:
                taste8 += int(c)

    return taste1,taste2,taste3,taste4,taste5,taste6,taste7,taste8


def taste_good(engine):
    df = pd.read_sql_table('jdsq', engine).loc[:, ['attribute', 'goodrate']]
    df = df.replace('', np.nan)
    df = df.dropna(how='any')
    df = df.drop_duplicates(keep='first')

    def taste_bar1(x):
        x1 = re.compile(",(.*?)味,")
        x2 = x1.findall(x)
        if len(x2) > 0:
            x2 = x2[0]
            x2 = str(x2)
            x2 = x2.split(',')
            x2 = x2[-1]
            x2 = str(x2) + '味'
            return x2
        else:
            return None
    df['attribute'] = df['attribute'].astype(str)
    df['attribute'] = df['attribute'].apply(taste_bar1)
    df['goodrate'] = df['goodrate'].astype(float)


    taste1 = []
    taste2 = []
    taste3 = []
    taste4 = []
    taste5 = []
    taste6 = []
    taste7 = []
    taste8 = []

    for p,c in zip(df['attribute'],df['goodrate']):
        if p is not None:
            if '混合口味' in p:
                taste1.append(float(c))
            if '牛肉味' in p:
                taste2.append(float(c))
            if '鸡肉味' in p:
                taste3.append(float(c))
            if '鸭肉味' in p:
                taste4.append(float(c))
            if '奶香味' in p:
                taste5.append(float(c))
            if '鱼肉味' in p:
                taste6.append(float(c))
            if '羊肉味' in p:
                taste7.append(float(c))
            if '水果味' in p:
                taste8.append(float(c))
    taste1 = np.array(taste1)
    taste1 = np.mean(taste1)

    taste2 = np.array(taste2)
    taste2 = np.mean(taste2)

    taste3 = np.array(taste3)
    taste3 = np.mean(taste3)

    taste4 = np.array(taste4)
    taste4 = np.mean(taste4)

    taste5 = np.array(taste5)
    taste5 = np.mean(taste5)

    taste6 = np.array(taste6)
    taste6 = np.mean(taste6)


    taste7 = np.array(taste7)
    taste7 = np.mean(taste7)

    taste8 = np.array(taste8)
    taste8 = np.mean(taste8)

    return taste1,taste2,taste3,taste4,taste5,taste6,taste7,taste8
