import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pandas as pd

df = pd.read_csv('./data/new_data.csv')


def main1(x):
    x1 = float(x)
    if x1 <= 1:
        return '1公里以内'
    elif 1 < x1 <= 2:
        return '1公里-2公里'
    elif 2 < x1 <= 3:
        return '2公里-3公里'
    elif 3 < x1 <= 4:
        return '3公里-4公里'
    elif 4 < x1 <= 5:
        return '4公里-5公里'
    else:
        return "5公里以上"


df['distance(单位:km)'] = df['distance(单位:km)'].apply(main1)


def main2(x):
    x1 = str(x).split(" ")
    x1 = x1[-1]
    x2 = str(x1).split(":")
    x2 = x2[1]
    if int(x2) < 10:
        return '骑行时间少于10分钟'
    elif 10 <= int(x2) <= 30:
        return '骑行时间10-30分钟以内'
    else:
        return '骑行时间大于30分钟'


df['sum_time'] = df['sum_time'].apply(main2)


def main3(x):
    x1 = int(x)
    if x1 == 0:
        return '星期天'
    elif x1 == 1:
        return '星期一'
    elif x1 == 2:
        return '星期二'
    elif x1 == 3:
        return '星期三'
    elif x1 == 4:
        return '星期四'
    elif x1 == 5:
        return '星期五'
    else:
        return '星期六'


df['week'] = df['week'].apply(main3)


def main4(x):
    x1 = int(x)
    if 0 <= x1 < 6:
        return '凌晨时段用车'
    elif 6 <= x1 < 12:
        return '早上时段用车'
    elif 12 <= x1 < 18:
        return '下午时段用车'
    else:
        return '晚上时段用车'


df['hour'] = df['hour'].apply(main4)


data1 = []
for j,k,l,o in zip(df['week'],df['hour'],df['sum_time'],df['distance(单位:km)']):
    data1.append([j,k,l,o])


te = TransactionEncoder()
df_tf = te.fit_transform(data1)
df = pd.DataFrame(df_tf,columns=te.columns_)
#min_support=0.3表示一个项集在数据集中出现的频率
frequent_itemsets = apriori(df,min_support=0.2,use_colnames= True)
rules = association_rules(frequent_itemsets,metric='confidence',min_threshold=0.15)
rules = rules.drop(rules[rules.lift <1.0].index)
rules.rename(columns={'antecedents':'前项','consequents':'后项','support':'支持度 %','confidence':'置信度 %','lift':'提升'},inplace = True)

data3 = pd.DataFrame(rules)
data3 = data3.drop(['antecedent support','consequent support','leverage','conviction'],axis=1)


def main5(x):
    x1 = str(x)
    x1 = x1.replace("frozenset(","").replace(")","")
    return x1


data3['前项'] = data3['前项'].apply(main5)
data3['后项'] = data3['后项'].apply(main5)

data3.sort_values(by=['置信度 %'],inplace=True,ascending=False)
data3.to_csv('./data/关联规则.csv',encoding='utf-8-sig',index=False)

