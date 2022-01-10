import pandas as pd
import sqlalchemy
import re
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn.metrics import r2_score
import joblib

engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/jd')


def price_line(engine):
    df = pd.read_sql_table('jdsq', engine).loc[:, ['price', 'comment','goodrate','poorrate','attribute']]
    df = df.replace('', np.nan)
    df = df.dropna(how='any')
    df = df.drop_duplicates(keep='first')

    def comment_number(x):
        x = str(x)
        x = x.replace('+','').replace('万','0000')
        return x
    df['price'] = df['price'].astype(float)
    df['comment'] = df['comment'].astype(str)
    df['comment'] = df['comment'].apply(comment_number)

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
    df['taste'] = df['attribute'].astype(str)
    df['taste'] = df['taste'].apply(taste_bar1)

    def brand_spilt(x):
        if "国产" in x:
            return "国产"
        elif "进口" in x:
            return "进口"
        else:
            return None
    def name_split(x):
        x = str(x)
        x = x.split(',')
        if x is not None:
            x = x[0]
            return x

    def weight_bar1(x):
        x1 = re.compile(",(.*?)kg,")
        x2 = x1.findall(x)
        if len(x2) > 0:
            x2 = x2[0]
            x2 = str(x2)
            x2 = x2.split(',')
            x2 = x2[-1]
            return x2
        else:
            return None
    df['brand'] = df['attribute'].astype(str)
    df['brand'] = df['brand'].apply(brand_spilt)
    df['goodrate'] = df['goodrate'].astype(float)
    # df['name'] = df['attribute'].astype(str)
    # df['name'] = df['name'].apply(name_split)
    df['weight'] = df['attribute'].astype(str)
    df['weight'] = df['weight'].apply(weight_bar1)
    df['comment'] = df['comment'].astype(int)
    df['weight'] = df['weight'].astype(float)
    df1 = df.drop(['poorrate','attribute'],axis=1)
    df1 = df1.replace(to_replace='None', value=np.NAN)
    df1 = df1.dropna(how='any')
    df1['brand'] = df1['brand'].replace('进口',1).replace('国产',0)
    # le = LabelEncoder()
    # df1['taste'] = le.fit_transform(df1['taste'])
    df1['taste'] = df1['taste'].replace('混合口味', 0).replace('牛肉味', 1).replace('鸡肉味', 2).replace('鸭肉味', 3).replace('鱼肉味', 4).replace('羊肉味', 5).replace('奶香味', 6).replace('水果味', 7).replace('海鲜味', 8)
    # cv = CountVectorizer()
    # df1['name'] = cv.fit_transform(df1['name'])

    data = df1.drop(['price'],axis=1)
    target = df1['price']
    train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.2)
    ss = preprocessing.StandardScaler()
    train_ss_x = ss.fit_transform(train_x)
    test_ss_x = ss.transform(test_x)
    # RFR = RandomForestRegressor()
    # RFR.fit(train_ss_x, train_y)
    # joblib.dump(RFR,'rfr.pkl')
    RFR = joblib.load('rfr.pkl')
    y_pred = RFR.predict(test_ss_x)
    score = r2_score(test_y, y_pred)
    score = "%0.2lf" % score
    x_data = [str(i) for i in range(len(test_y))]
    test_y = [x for x in test_y]
    y_pred = [x for x in y_pred]
    return test_y,y_pred,x_data,score,test_x




