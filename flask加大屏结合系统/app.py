import os
import sys
from datetime import timedelta
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from flask import Flask, render_template
from data import SourceData
from flask import *
from bigdata import SourceData1

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
            return render_template('index.html', form=data,title=data.title,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8)
    return render_template('register.html')


@app.route('/big_screen')
def index2():
    data = SourceData1()
    comments = data.comment
    return render_template('big_screen.html', form=data, title=data.title, comments=comments)


@app.route('/word')
def word():
    data = SourceData()
    return render_template('word.html', form=data,title=data.title,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8)


@app.route('/barh')
def barh():
    data = SourceData()
    return render_template('barh.html', form=data,title=data.title,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8)


@app.route('/pie')
def pie():
    data = SourceData()
    return render_template('pie.html', form=data,title=data.title,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8)


@app.route('/radius1')
def radius1():
    data = SourceData()
    return render_template('radius1.html', form=data,title=data.title,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8)


@app.route('/radius2')
def radius2():
    data = SourceData()
    return render_template('radius2.html', form=data,title=data.title,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8)


@app.route('/radius3')
def radius3():
    data = SourceData()
    return render_template('radius3.html', form=data,title=data.title,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8)


@app.route('/radius4')
def radius4():
    data = SourceData()
    return render_template('radius4.html', form=data,title=data.title,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
