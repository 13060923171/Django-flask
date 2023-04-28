import os
import sys
from datetime import timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from flask import Flask, render_template
from data import SourceData
from flask import *
import pandas as pd

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

name = ''
login = ''
@app.route('/', methods=('GET', 'POST'))
def index():
    global name, login
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'admin':
            login = 'success'
            name = 'admin'
            data = SourceData()
            return render_template('index.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)
    return render_template('register.html')


@app.route('/pie1')
def pie1():
    data = SourceData()
    return render_template('pie1.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/pie2')
def pie2():
    data = SourceData()
    return render_template('pie2.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/pie3')
def pie3():
    data = SourceData()
    return render_template('pie3.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/barh1')
def barh1():
    data = SourceData()
    return render_template('barh1.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/barh2')
def barh2():
    data = SourceData()
    return render_template('barh2.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/line')
def line():
    data = SourceData()
    return render_template('line.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/picture')
def picture():
    data = SourceData()
    return render_template('picture.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/table')
def table():
    data = SourceData()
    df = pd.read_csv('./data/关联规则.csv')
    labels = []
    for j, k, l, i, o in zip(df['前项'], df['后项'], df['支持度 %'], df['置信度 %'], df['提升']):
        result = {}
        result["antecedents"] = j
        result["consequents"] = k
        result["support"] = l
        result["confidence"] = i
        result["lift"] = o
        labels.append(result)
    return render_template('table.html',form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,labels=labels,title9=data.title9)

@app.route('/map')
def map():
    data = SourceData()
    return render_template('map.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
