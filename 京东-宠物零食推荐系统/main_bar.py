import pandas as pd
import sqlalchemy

# engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/jd')


def price_bar(engine):
    df = pd.read_sql_table('jdsq', engine).loc[:, ['price', 'comment','goodrate','poorrate','attribute']]
    df = df.drop_duplicates(keep='first')
    price = df['price'].astype(float)
    data1 = len(price[price <= 100])
    data2 = len(price[(price > 100) & (price <= 200)])
    data3 = len(price[(price > 200) & (price <= 300)])
    data4 = len(price[(price > 300) & (price <= 400)])
    data5 = len(price[(price > 400) & (price <= 500)])
    data6 = len(price[price >= 500])

    return data1,data2,data3,data4,data5,data6

