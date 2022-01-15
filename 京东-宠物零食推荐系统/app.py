#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template,request
from data import SourceData
import pymysql
from suggest import merchant,buyer
import joblib
from sklearn import preprocessing
from main_line import price_line
import numpy as np
import pandas as pd
import sqlalchemy


app = Flask(__name__)

name = ''
login = ''

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    db='jd',
    charset='utf8'
)



@app.route('/')
def index():
    data = SourceData()
    return render_template('index.html', form=data, title=data.title)


@app.route('/sql', methods=['GET', 'POST'])
def show_sql():
    if request.method == 'POST':
        number = request.values.get('limit')
        order = request.values.get('order')
        source = request.values.get('source')
        taste = request.values.get('taste')
        variety = request.values.get('variety')
        if number is not None and order is not None and source is not None and taste is not None and variety is not None:
            if number == "--请选择展示的数量--":
                number = 20
            if order == "--请选择排序的顺序--":
                order = ''
            if order == "从高到低":
                order = 'ORDER BY price'
            if order == "从低到高":
                order = 'ORDER BY price DESC'
            if source == "--请选择来源类型--":
                source = ''
                if taste == "--请选择口味--":
                    taste = ''
                if taste == "混合口味":
                    taste = "WHERE attribute LIKE '%混合口味%'"
                if taste == "牛肉味":
                    taste = "WHERE attribute LIKE '%牛肉味%'"
                if taste == "鸡肉味":
                    taste = "WHERE attribute LIKE '%鸡肉味%'"
                if taste == "鸭肉味":
                    taste = "WHERE attribute LIKE '%鸭肉味%'"
                if taste == "奶香味":
                    taste = "WHERE attribute LIKE '%奶香味%'"
                if taste == "鱼肉味":
                    taste = "WHERE attribute LIKE '%鱼肉味%'"
                if taste == "羊肉味":
                    taste = "WHERE attribute LIKE '%羊肉味%'"
                if taste == "水果味":
                    taste = "WHERE attribute LIKE '%水果味%'"
            if source == "国产":
                source = "WHERE attribute LIKE '%国产%'"
                if taste == "--请选择口味--":
                    taste = ''
                if taste == "混合口味":
                    taste = "and attribute LIKE '%混合口味%'"
                if taste == "牛肉味":
                    taste = "and attribute LIKE '%牛肉味%'"
                if taste == "鸡肉味":
                    taste = "and attribute LIKE '%鸡肉味%'"
                if taste == "鸭肉味":
                    taste = "and attribute LIKE '%鸭肉味%'"
                if taste == "奶香味":
                    taste = "and attribute LIKE '%奶香味%'"
                if taste == "鱼肉味":
                    taste = "and attribute LIKE '%鱼肉味%'"
                if taste == "羊肉味":
                    taste = "and attribute LIKE '%羊肉味%'"
                if taste == "水果味":
                    taste = "and attribute LIKE '%水果味%'"
            if source == "进口":
                source = "WHERE attribute LIKE '%进口%'"
                if taste == "--请选择口味--":
                    taste = ''
                if taste == "混合口味":
                    taste = "and attribute LIKE '%混合口味%'"
                if taste == "牛肉味":
                    taste = "and attribute LIKE '%牛肉味%'"
                if taste == "鸡肉味":
                    taste = "and attribute LIKE '%鸡肉味%'"
                if taste == "鸭肉味":
                    taste = "and attribute LIKE '%鸭肉味%'"
                if taste == "奶香味":
                    taste = "and attribute LIKE '%奶香味%'"
                if taste == "鱼肉味":
                    taste = "and attribute LIKE '%鱼肉味%'"
                if taste == "羊肉味":
                    taste = "and attribute LIKE '%羊肉味%'"
                if taste == "水果味":
                    taste = "and attribute LIKE '%水果味%'"
            if variety == "--请选择狗/猫--":
                variety = 'jdsq'
            if variety == "狗":
                variety = "(SELECT * FROM jdsq WHERE attribute LIKE '%狗%') as variety"
            if variety == "猫":
                variety = "(SELECT * FROM jdsq WHERE attribute LIKE '%猫%') as variety"

            # get annual sales rank
            cur = conn.cursor()
            sql = "select * from {} {} {} {} LIMIT {}".format(variety,source, taste, order, number)
            cur.execute(sql)
            content = cur.fetchall()

            # 获取表头
            sql = "SHOW FIELDS FROM jdsq"
            cur.execute(sql)
            labels = cur.fetchall()
            labels = [l[0] for l in labels]
            return render_template('jd_sql.html', labels=labels, content=content)

        cur = conn.cursor()
        # get annual sales rank
        sql = "select * from jdsq LIMIT 50"
        cur.execute(sql)
        content = cur.fetchall()

        # 获取表头
        sql = "SHOW FIELDS FROM jdsq"
        cur.execute(sql)
        labels = cur.fetchall()
        labels = [l[0] for l in labels]
        return render_template('jd_sql.html', labels=labels, content=content)


@app.route('/suggest', methods=['GET', 'POST'])
def give_suggest():
    if request.method == 'POST':
        price1, price2, brand, taste1, taste2, taste3, str_word = merchant()
        taste11, price11, brand11,word11 = buyer()
        return render_template('suggest.html',price1=price1,price2=price2,brand=brand,taste1=taste1,taste2=taste2,
                               taste3=taste3,word1=str_word,taste11=taste11,price11=price11,brand11=brand11,word11=word11)


@app.route('/test', methods=['GET', 'POST'])
def test():
    engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/jd')
    test_y, y_pred, x_data, score,test_x = price_line(engine)

    def comment_number(x):
        x = str(x)
        x = x.replace('+','').replace('万','0000')
        return x
    global name,login
    if request.method == 'POST':
        if request.form.get('comment') != None and request.form.get('goodrate') != None and request.form.get('taste') != None and request.form.get('brand') != None and request.form.get('kg') != None:
            comment = request.form.get('comment')
            comment1 = comment_number(comment)
            goodrate = request.form.get('goodrate')
            goodrate1 = float(goodrate)
            taste = request.form.get('taste')
            taste1 = str(taste).replace('混合口味', '0').replace('牛肉味', '1').replace('鸡肉味', '2').replace('鸭肉味', '3').replace('鱼肉味', '4').replace('羊肉味', '5').replace('奶香味', '6').replace('水果味', '7').replace('海鲜味', '8')
            brand = request.form.get('brand')
            brand1 = str(brand).replace('进口','1').replace('国产','0')
            kg = request.form.get('kg')
            kg1 = float(kg)

            price = np.array([comment1, goodrate1, float(taste1), float(brand1), kg1])
            test_x = np.append(test_x, [price], axis=0)
            ss = preprocessing.StandardScaler()
            test_price = ss.fit_transform(test_x)
            RFR = joblib.load('rfr.pkl')
            price_pred = RFR.predict(test_price)
            price_pred = "%0.2lf" %(price_pred[-1])
            login = 'success'
            name = 'admin'
            return render_template('price.html', name=name, login=login,comment=comment,goodrate=goodrate,taste=taste,brand=brand,kg=kg,price=price_pred)

    return render_template('price_predict.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
