from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
df = pd.read_csv('mobike_shanghai_sample_updated.csv')


#公式计算两点间距离（m）
def geodistance(lng1,lat1,lng2,lat2):
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)]) # 经纬度转换成弧度
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
    distance=round(distance/1000,3)
    return distance

distance = []
for h,j,k,l in zip(df['start_location_x'],df['start_location_y'],df['end_location_x'],df['end_location_y']):
    km = geodistance(h,j,k,l)
    km = round(km,4)
    distance.append(km)

df['distance(单位:km)'] = distance
df['sum_time'] = pd.to_datetime(df['end_time']) - pd.to_datetime(df['start_time'])

weekday = []
for i in pd.to_datetime(df['end_time']):
    weekday.append(i.weekday())

df['week'] = weekday

def main1(x):
    x1 = str(x)
    x1 = x1.split(' ')
    x1 = x1[-1]
    x2 = str(x1).split(":")
    x2 = x2[0]
    return x2

df['hour'] = pd.to_datetime(df['end_time']).apply(main1)


df.to_csv('new_data.csv',encoding='utf-8-sig',index=False)
