import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/jd')


def production_map(engine):
    df = pd.read_sql_table('jdsq', engine).loc[:, ['price', 'comment', 'goodrate', 'poorrate', 'attribute']]
    df = df.drop_duplicates(keep='first')

    def production_spilt(x):
        x = str(x)
        x = x.split(',')
        if len(x) >=4:
            x = x[3]
            return x
        else:
            return None
    df['attribute'] = df['attribute'].astype(str)
    production = df['attribute'].apply(production_spilt)
    production_list = []
    for p in production:
        p = str(p)
        if "No" not in p:
            if 'kg' in p or '1' in p or '0' in p:
                pass
            else:
                p = p[-2:]
                production_list.append(p)
    counts = {}
    for s in production_list:
        counts[s] = counts.get(s, 0) + 1

    data1 = []
    for key,values in counts.items():
        d = {
            'name': key, 'value': values,
        }
        data1.append(d)

    return data1

