import os
import sys
from datetime import timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from flask import Flask, render_template
from data import SourceData
from flask import *

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
            return render_template('index.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9,title10=data.title10)
    return render_template('register.html')


@app.route('/line')
def line():
    data = SourceData()
    return render_template('line.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9,title10=data.title10)


@app.route('/word')
def word():
    data = SourceData()
    return render_template('word.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9,title10=data.title10)


@app.route('/barh')
def barh():
    data = SourceData()
    return render_template('barh.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9,title10=data.title10)


@app.route('/pie')
def pie():
    data = SourceData()
    return render_template('pie.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9,title10=data.title10)


@app.route('/radius1')
def radius1():
    data = SourceData()
    return render_template('radius1.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9,title10=data.title10)


@app.route('/radius2')
def radius2():
    data = SourceData()
    return render_template('radius2.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9,title10=data.title10)


@app.route('/radius3')
def radius3():
    data = SourceData()
    return render_template('radius3.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9,title10=data.title10)


@app.route('/radius4')
def radius4():
    data = SourceData()
    return render_template('radius4.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9,title10=data.title10)

@app.route('/picture')
def picture():
    data = SourceData()
    return render_template('picture.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9,title10=data.title10)

@app.route('/number')
def number():
    data = SourceData()
    moon_mean, week_mean, day_sum,content = data.echart6
    data1 = data.echart4
    pos_number = None
    neg_number = None
    for d in data1:
        if d['name'] == 'pos':
            pos_number = d['value']
        if d['name'] == 'neg':
            neg_number = d['value']
    sum_number = pos_number + neg_number
    title12 = '新增舆情'
    users = content
    return render_template('number.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,
                           title9=data.title9,title10=data.title10,moon_mean=moon_mean,week_mean=week_mean,day_sum=day_sum,users=users,title12 = title12,pos_number=pos_number,neg_number=neg_number,sum_number=sum_number)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
