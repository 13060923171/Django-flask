import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType


def main(name):
    df = data[data['关键词'] == name]
    new_df = df['会员类型'].value_counts()
    x_data = [n for n in new_df.index]
    y_data = [n for n in new_df.values]

    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add(
            "",
            [(j,int(k)) for j,k in zip(x_data, y_data)],
            radius=["40%", "55%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{b}: {c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="{}-会员类型".format(name)))
            .render("./templates/{}-会员类型.html".format(name))
    )


if __name__ == '__main__':
    data = pd.read_excel('./demo/data/微博数据.xlsx')
    name_data = data['关键词'].value_counts()
    x_data1 = [n for n in name_data.index]
    for o in x_data1:
        main(o)