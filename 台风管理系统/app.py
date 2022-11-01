import os
import sys
from flask import Flask, render_template,request
from crawl import acquire_data
import datetime
from tqdm import tqdm
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/crwal', methods=['GET', 'POST'])
def crwal1():
    if request.method == 'POST':
        word_data = []
        dic = {
            '莫兰蒂': ['2016-09-10', '2016-09-18'],
            '灿都': ['2021-09-07', '2021-09-20'],
            '马鞍': ['2022-08-22', '2022-08-28'],
            '梅花': ['2022-09-08', '2022-09-18']

        }
        for wor in tqdm(dic.keys()):
            for ti in dic.values():
                k = ti[0]
                j = ti[1]  # 设置范围
                dates = []
                dt = datetime.datetime.strptime(k, "%Y-%m-%d")
                date = k[:]
                while date <= j:
                    dates.append(date)
                    dt = dt + datetime.timedelta(1)
                    date = dt.strftime("%Y-%m-%d")
                for tii in dates:  # 循环这一年的每天
                    words = [wor, tii]
                    acquire_data(words)
        return render_template('Crwal.html', title='运行完毕')


@app.route('/sql', methods=['GET', 'POST'])
def select_name():
    if request.method == 'POST':
        name = request.values.get('limit')
        if name == '灿都':
            return render_template('page.html', name='灿都', title='灿都台风-数据分析')
        if name == '马鞍':
            return render_template('page.html', name='马鞍', title='马鞍台风-数据分析')
        if name == '梅花':
            return render_template('page.html', name='梅花', title='梅花台风-数据分析')
        if name == '莫兰蒂':
            return render_template('page.html', name='莫兰蒂', title='莫兰蒂台风-数据分析')


@app.route('/灿都-LDA主题模型')
def lda1():
    return render_template('灿都-LDA主题模型.html', title='灿都台风-数据分析')


@app.route('/灿都-词云')
def word1():
    return render_template('灿都-词云.html', title='灿都台风-数据分析')


@app.route('/灿都-会员类型')
def type1():
    return render_template('灿都-会员类型.html', title='灿都台风-数据分析')


@app.route('/灿都-数据指标变化趋势')
def line1():
    return render_template('灿都-数据指标变化趋势.html', title='灿都台风-数据分析')


@app.route('/马鞍-LDA主题模型')
def lda2():
    return render_template('马鞍-LDA主题模型.html', title='马鞍台风-数据分析')


@app.route('/马鞍-词云')
def word2():
    return render_template('马鞍-词云.html', title='马鞍台风-数据分析')


@app.route('/马鞍-会员类型')
def type2():
    return render_template('马鞍-会员类型.html', title='马鞍台风-数据分析')


@app.route('/马鞍-数据指标变化趋势')
def line2():
    return render_template('马鞍-数据指标变化趋势.html', title='马鞍台风-数据分析')


@app.route('/梅花-LDA主题模型')
def lda3():
    return render_template('梅花-LDA主题模型.html', title='梅花台风-数据分析')


@app.route('/梅花-词云')
def word3():
    return render_template('梅花-词云.html', title='梅花台风-数据分析')


@app.route('/梅花-会员类型')
def type3():
    return render_template('梅花-会员类型.html', title='梅花台风-数据分析')


@app.route('/梅花-数据指标变化趋势')
def line3():
    return render_template('梅花-数据指标变化趋势.html', title='梅花台风-数据分析')


@app.route('/莫兰蒂-LDA主题模型')
def lda4():
    return render_template('莫兰蒂-LDA主题模型.html', title='莫兰蒂台风-数据分析')


@app.route('/莫兰蒂-词云')
def word4():
    return render_template('莫兰蒂-词云.html', title='莫兰蒂台风-数据分析')


@app.route('/莫兰蒂-会员类型')
def type4():
    return render_template('莫兰蒂-会员类型.html', title='莫兰蒂台风-数据分析')


@app.route('/莫兰蒂-数据指标变化趋势')
def line4():
    return render_template('莫兰蒂-数据指标变化趋势.html', title='莫兰蒂台风-数据分析')


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
