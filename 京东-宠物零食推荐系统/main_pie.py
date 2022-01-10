import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/jd')


def brand_pie(engine):
    df = pd.read_sql_table('jdsq', engine).loc[:, ['price', 'comment', 'goodrate', 'poorrate', 'attribute']]
    df = df.drop_duplicates(keep='first')

    def brand_spilt(x):
        if "国产" in x:
            return "国产"
        elif "进口" in x:
            return "进口"
        else:
            return None
    df['attribute'] = df['attribute'].astype(str)
    brand = df['attribute'].apply(brand_spilt)
    brand = brand.value_counts()
    data_pair_1 = [(i, int(j)) for i, j in zip(brand.index, brand.values)]
    data_pair_1.sort(key=lambda x: x[1], reverse=True)
    # return data_pair_1[0][0]
    return data_pair_1

# def brand_pie1():
#     data_pair_1 = brand_pie()
#     data_pair_1.sort(key=lambda x: x[1], reverse=True)
#     return data_pair_1[0][0]
