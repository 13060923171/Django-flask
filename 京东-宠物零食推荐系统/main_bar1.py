import pandas as pd
import sqlalchemy
import numpy as np

# engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/jd')


def comment_bar(engine):
    df = pd.read_sql_table('jdsq', engine).loc[:, ['price', 'comment']]
    df = df.replace('', np.nan)
    df = df.dropna(how='any')

    def comment_number(x):
        x = str(x)
        x = x.replace('+','').replace('万','0000')
        return x
    df['price'] = df['price'].astype(float)

    df['comment'] = df['comment'].astype(str)
    df['comment'] = df['comment'].apply(comment_number)

    sum_100 = 0
    sum_200 = 0
    sum_300 = 0
    sum_400 = 0
    sum_500 = 0
    sum_600 = 0
    for p,c in zip(df['price'],df['comment']):
        if int(p) <= 100:
            sum_100 += int(c)
        elif 100 < int(p) <= 200:
            sum_200 += int(c)
        elif 200 < int(p) <= 300:
            sum_300 += int(c)
        elif 300 < int(p) <= 400:
            sum_400 += int(c)
        elif 400 < int(p) <= 500:
            sum_500 += int(c)
        else:
            sum_600 += int(c)

    return sum_100,sum_200,sum_300,sum_400,sum_500,sum_600


def price_good(engine):
    df = pd.read_sql_table('jdsq', engine).loc[:, ['price', 'goodrate']]
    df = df.replace('', np.nan)
    df = df.dropna(how='any')

    df['price'] = df['price'].astype(float)
    df['goodrate'] = df['goodrate'].astype(float)

    sum_100 = []
    sum_200 = []
    sum_300 = []
    sum_400 = []
    sum_500 = []
    sum_600 = []

    for p,c in zip(df['price'],df['goodrate']):
        if int(p) <= 100:
            sum_100.append(float(c))
        elif 100 < int(p) <= 200:
            sum_200.append(float(c))
        elif 200 < int(p) <= 300:
            sum_300.append(float(c))
        elif 300 < int(p) <= 400:
            sum_400.append(float(c))
        elif 400 < int(p) <= 500:
            sum_500.append(float(c))
        else:
            sum_600.append(float(c))

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

    sum_600 = np.array(sum_600)
    sum_600 = np.mean(sum_600)

    return sum_100,sum_200,sum_300,sum_400,sum_500,sum_600

