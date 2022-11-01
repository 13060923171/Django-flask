import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import numpy as np

def main(name):
    df = data[data['关键词'] == name]
    def date_xiugai(x):
        x1 = str(x)
        if '年' not in x1:
            x1 = '2022年' + x1
            return x1
        else:
            return x1

    df['发布时间'] = df['发布时间'].apply(date_xiugai)


    def date_tihuan(i):
        i = str(i).split('日')
        i = i[0]
        p = pd.to_datetime(i,format='%Y年%m月%d')
        return p


    df['时间'] = df['发布时间'].apply(date_tihuan)

    df.Timestamp = pd.to_datetime(df['时间'])
    df.index = df.Timestamp

    if name == '灿都':
        df = df['2021-09-07':'2021-09-20']
        df_Q = df.resample('D').sum()
    elif name == '马鞍':
        df = df['2022-08-22':'2022-08-28']
        df_Q = df.resample('D').sum()
    elif name == '梅花':
        df = df['2022-09-08':'2022-09-18']
        df_Q = df.resample('D').sum()
    else:
        df = df['2016-09-10':'2016-09-18']
        df_Q = df.resample('D').sum()

    x_data = ['第一天','第二天','第三天','第四天','第五天','第六天','第七天']
    # for j in df_Q.index:
    #     j = str(j).split('-')
    #     x_data.append(j[0])

    y_data1 = []
    for k in df_Q['转发数']:
        y_data1.append(k)

    y_data2 = []
    for k in df_Q['评论数']:
        y_data2.append(k)

    y_data3 = []
    for k in df_Q['点赞数']:
        y_data3.append(k)

    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="转发",
            symbol="emptyCircle",
            is_symbol_show=False,
            color="#ADFF2F",
            y_axis=y_data1[0:7],
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=3)
        )
            .add_yaxis(
            series_name="评论",
            symbol="emptyCircle",
            is_symbol_show=False,
            color="#00FA9A",
            y_axis=y_data2[0:7],
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=3)
        )
            .add_yaxis(
            series_name="点赞",
            symbol="emptyCircle",
            is_symbol_show=False,
            color="#00FA9A",
            y_axis=y_data3[0:7],
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=3)
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="{}-数据指标变化趋势".format(name)),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False,axisline_opts=opts.AxisLineOpts(
                is_on_zero=False,
            )),
        )
            .render("./demo/{}-数据指标变化趋势.html".format(name))
    )


if __name__ == '__main__':
    data = pd.read_excel('./demo/data/微博数据.xlsx')
    name_data = data['关键词'].value_counts()
    x_data1 = [n for n in name_data.index]
    for o in x_data1:
        main(o)