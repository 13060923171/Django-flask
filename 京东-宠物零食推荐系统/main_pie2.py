import pandas as pd
import sqlalchemy
import numpy as np
engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/jd')


def goodrate_pie(engine):
    df = pd.read_sql_table('jdsq', engine).loc[:, ['goodrate', 'attribute']]
    df = df.replace('', np.nan)
    df = df.dropna(how='any')
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
    goodrate = df['goodrate'].astype(float)
    domestic_list = []
    import_list = []
    for b,g in zip(brand,goodrate):
        if b == '国产':
            domestic_list.append(g)
        if b == '进口':
            import_list.append(g)
    domestic = np.array(domestic_list)
    domestic = np.mean(domestic)
    import1 = np.array(import_list)
    import1 = np.mean(import1)

    domestic = domestic * 100
    domestic = '%0.2lf' % domestic
    domestic_2 = '%0.2lf' % (100 - float(domestic))

    import1 = import1 * 100
    import1 = '%0.2lf' % import1
    import_2 = '%0.2lf' % (100 - float(import1))
    return domestic,domestic_2,import1,import_2

