import os
import sys
from datetime import timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from flask import Flask, render_template
from data import SourceData

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@app.route('/')
def index():
    data = SourceData()
    return render_template('index.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/line')
def line():
    data = SourceData()
    return render_template('line.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/word')
def word():
    data = SourceData()
    return render_template('word.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/barh')
def barh():
    data = SourceData()
    return render_template('barh.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/pie')
def pie():
    data = SourceData()
    return render_template('pie.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/radius1')
def radius1():
    data = SourceData()
    return render_template('radius1.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/radius2')
def radius2():
    data = SourceData()
    return render_template('radius2.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/radius3')
def radius3():
    data = SourceData()
    return render_template('radius3.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


@app.route('/radius4')
def radius4():
    data = SourceData()
    return render_template('radius4.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)

@app.route('/picture')
def picture():
    data = SourceData()
    return render_template('picture.html', form=data,title=data.title,title1=data.title1,title2=data.title2,title3=data.title3,title4=data.title4,title5=data.title5,title6=data.title6,title7=data.title7,title8=data.title8,title9=data.title9)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
