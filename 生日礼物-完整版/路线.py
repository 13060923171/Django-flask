from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pyecharts.globals import ThemeType


c = (
    Geo(init_opts=opts.InitOpts(width="1080px",theme=ThemeType.LIGHT))
    .add_coordinate(name="Melbourne", longitude=144.57, latitude=-37.48)
    .add_coordinate(name="Beijing", longitude=116.3, latitude=39.9)
    .add_schema(
        maptype="world",
        itemstyle_opts=opts.ItemStyleOpts(color="#323c48", border_color="#111"),
    )
    .add(
        "",
        [("Melbourne", 9.132),("Beijing",0)],
        type_=ChartType.EFFECT_SCATTER,
        color="white",
        label_opts=opts.LabelOpts(is_show=False)
    )
    .add(
        "",
        [("Melbourne", "Beijing")],
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=12, color="blue",trail_length=0.5
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
        label_opts=opts.LabelOpts(is_show=False)
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
        title_opts=opts.TitleOpts(
            title="9,123千米这是我们之间的距离",
            pos_left="center",
            pos_top="top",
            title_textstyle_opts=opts.TextStyleOpts(
                font_size=25, color="rgba(47, 7, 19, 0.9)"
            ),
        ),)
    .render("geo_lines_background.html")
)

