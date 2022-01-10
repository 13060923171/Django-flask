import requests
from lxml import etree
from urllib import parse
import json
import re
from tqdm import tqdm
import time
import random
from jd_sql import COMMODITY,sess


user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

headers = {

    'user-agent': random.choice(user_agent),
    'referer': 'https://www.jd.com/',
    'cookie': '__jdu=161827796288293166331; shshshfpa=afbfb5a6-2b2f-2cd1-32c9-08f6cb7b5e62-1618277978; shshshfpb=bUxR1wpyM7eG3WPxMIY3taQ%3D%3D; qrsc=3; __jdv=122270672|google|AmericaBrandC013|cpc|notset|1640315908058; areaId=19; unpl=JF8EAJtnNSttDEsADEkHGEUTGVVSW10BS0dRazJSA10PSgcFTlYdRxh7XlVdXRRLFB9tZxRUXFNPVw4YCisSEHtdVV9eDkIQAmthNWRVUCVUSBtsGHwQBhAZbl4IexcCX2cCVFRbTVINHAESGxNDX1RZWgpJFzNfZwNkbWhKZAQrAytZfkoQVFldAUgRBWdgBl1UW0NWBRwFGRAQe1xkXQ; PCSYCityID=CN_440000_440100_0; __jda=122270672.161827796288293166331.1618277963.1640315908.1640919150.13; __jdc=122270672; rkv=1.0; ip_cityCode=1601; ipLoc-djd=19-1601-50258-51885; wlfstk_smdl=oocykpch3wbi1g1kjdkau6t4hg8xn1xb; pinId=01r_11wrtu-px-RD9rxzTA; pin=13060923171_p; ceshi3.com=000; _tp=WNcwuIzQXfELh%2FoEGttAMw%3D%3D; _pst=13060923171_p; token=8ce4c63baaecd8874df2b7c6b0675594,3,911622; __tk=jDnDIsJTjsjDJsbpkDJqlUaFJcuqlskijzfhkcj5Jce5jzeyIzqxJn,3,911622; shshshfp=cf38c8abbccba81cd90a9b0533d2397b; shshshsID=da44cdd3cafbdf7190fa00d806f19252_9_1640920582478; __jdb=122270672.12.161827796288293166331|13.1640919150; thor=9CDF719556DCA01F6CA5CCD738DD5ADDD16FD6132EA3879F4E435E7C3B8C2E5A77ADD97056B6C99F17924668D0297D494B640CCAB3F74C820190A0F6E78AAABDB49B834EEDD997723D3E7D176A01D2F09CBC8069924AB954ADC9EF258C36B9985E0919ED3063252A70841F2FA5C60BDB60B70A096AA72E19289D6A669F63E87760BC79E9D32FDC47006C9B2EC5D25138; 3AB9D23F7A4B3C9B=VXCREJHRBERJFNRSY7JQ5GDZ3XXG3TDRDLBEPH5N3QML3Y3RHTZRTEUTUJ3EE3LZOZRXXFF2ZTMB7NKN2N7PBKKTUA',

}


KEYWORD = parse.quote('宠物零食')
#长连接，就是把几个请求连接起来变成一个，防止对那个网站损害太大
session = requests.session()
session.headers = headers

def get_parse(url):
    html = session.get(url)
    if html.status_code == 200:
        get_html(html)
        a = random.random()
        time.sleep(a)
    else:
        print(html.status_code)

def get_html(html):
    content = html.text
    soup = etree.HTML(content)
    items = soup.xpath("//div[@class='gl-i-wrap']")
    for i in range(len(items)):
        #获取好评连接的通道
        href = soup.xpath("//div[@class='p-img']/a[@target='_blank']/@href")[i]
        #商品详细页面
        href = 'https:' + href
        commit = re.compile('https://item.jd.com/(.*?).html',re.S|re.I)
        commits = commit.findall(href)
        #返回好评和差评的占比
        comment,goodrate,poorrate = get_number(commits[0])
        #价格
        price = soup.xpath("//div[@class='p-price']/strong/i/text()")[i]
        a = random.random()
        time.sleep(a)
        get_comment(href,price,comment,goodrate,poorrate)


def get_number(commits):
    url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'.format(commits)
    headers = {
        "Cookie": "__jdu=1640258720578828922910; shshshfpa=10d886ae-c8ba-32c1-dec7-115bdc597c96-1611631742; PCSYCityID=CN_440000_440100_0; shshshfpb=vO8kcng5CBeDAG2jENl%2B7KQ%3D%3D; areaId=19; ipLoc-djd=19-1601-50258-51885; mt_xid=V2_52007VwMVV1xbVlMZShhYA24KEVtVW1FSH0gpDFY3VxVXXQhODxkaG0AANARGTg5dUVsDHBFUBmILE1tdXVddL0oYXwZ7AhJOXFxDWhdCGlUOYwEiUm1YYl4ZSxFeAWMEElVtXFZZHQ%3D%3D; unpl=JF8EAJ1nNSttWxxdDRpSGhAXTFkBWw1cTkQHamMEVFkKH1cNE1EfRhB7XlVdXhRKFx9uYxRUVVNPVA4YBisSEHtdVV9eDkIQAmthNWRVUCVUSBtsGHwQBhAZbl4IexcCX2cCUVxbT10DGAMfFBlCXl1WXgtDFwJfVwVSbWh7VTUaMhoiWyVcGV5aDUoUB2ZhBlVZXkJdBhIKGBEYS1xkX20L; __jdv=122270672|direct|-|none|-|1641661318623; __jda=122270672.1640258720578828922910.1640258721.1641661319.1641697056.8; __jdc=122270672; shshshfp=54d96a259681e1eba8c936e3c8ed6997; ip_cityCode=1601; jwotest_product=99; token=d5e0e583ec860620f78b060c0ab6292b,2,912054; __tk=2uaArc2WqY1F1zaE2Ytt2wyW1wWWrYqn2YMDqDM31zSnqYfErASn1M,2,912054; 3AB9D23F7A4B3C9B=YQGWPJUHPQUE6WZPZAG6HUZYQ4LZEJOGPZFJ23EKN627VOCZSGABUYQ5HZF5Z72LN4IWU4P4I5JE2B6EC7R4ER64Z4; JSESSIONID=CECAE456F566A7861DC285818DD97DC5.s1; shshshsID=4a108baf005b299ecea235deb648e0e3_11_1641697803765; __jdb=122270672.11.1640258720578828922910|8.1641697056",
        'Host': 'club.jd.com',
        'Referer': 'https://item.jd.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    html = requests.get(url,headers=headers)
    a = random.random()
    time.sleep(a)
    content = html.text
    #评论的数据
    comment = re.compile('"CommentCountStr":"(.*?)",', re.I | re.S)
    comments = comment.findall(content)
    try:
        comments = comments[0]
    except:
        comments = ''
    #好评的占比
    goodrate = re.compile('"GoodRate":(.*?),', re.I | re.S)
    goodrates = goodrate.findall(content)
    try:
        goodrates = goodrates[0]
    except:
        goodrates = ''
    #差评的占比
    poorrate = re.compile('"GeneralRate":(.*?),', re.I | re.S)
    poorrates = poorrate.findall(content)
    try:
        poorrates = poorrates[0]
    except:
        poorrates = ''
    a = random.random()
    time.sleep(a)
    return comments,goodrates,poorrates


def get_comment(url,price,comment,goodrate,poorrate):
    html = session.get(url)
    a = random.random()
    time.sleep(a)
    content = html.text
    soup = etree.HTML(content)
    attribute = soup.xpath("//ul[@class='parameter2 p-parameter-list']/li/@title")
    if len(attribute) > 0:
        atr = ','.join(attribute)
    else:
        atr = None
    try:
        sp_data = COMMODITY(
            price=price,
            comment=comment,
            goodrate=goodrate,
            poorrate=poorrate,
            attribute=atr
        )
        sess.add(sp_data)
        sess.commit()
    except Exception as e:
        print(e)
        sess.rollback()


# #写一个保存文件的函数
# def save_to_file(result):
#     #a是追加信息的意思
#     with open("商品属性1.text","a",encoding='utf-8') as f:
#         #把python转化为json，然后用json的形式保存下来，ensure_ascii=False是识别有没有中文的意思
#         f.write(json.dumps(result,ensure_ascii=False)+"\n")
#         print("存储到text成功")


if __name__ == '__main__':
    list1 = []
    for i in range(1,200,2):
        list1.append(i)
    list2 = [1,57]
    for j in range(116,5937,60):
        list2.append(j)
    for l in tqdm(range(len(list2))):
        url = 'https://search.jd.com/Search?keyword={}&qrst=1&wq={}&shop=1&pvid=e6ecffa80f704a8c920bfb64c6e96752&page={}&s={}&click=0'.format(KEYWORD,KEYWORD,list1[l],list2[l])
        get_parse(url)
        a = random.random()
        time.sleep(a)

    # list1 = []
    # for i in range(1, 3, 2):
    #     list1.append(i)
    # list2 = [1]
    # # for j in range(56, 5937, 60):
    # #     list2.append(j)
    # for l in tqdm(range(len(list2))):
    #     url = 'https://search.jd.com/Search?keyword={}&wq={}={}&s={}&click=0'.format(KEYWORD, KEYWORD, list1[l],
    #                                                                                  list2[l])
    #     get_parse(url)

#https://search.jd.com/Search?keyword=%E5%AE%A0%E7%89%A9%E9%9B%B6%E9%A3%9F&qrst=1&wq=%E5%AE%A0%E7%89%A9%E9%9B%B6%E9%A3%9F&stock=1&pvid=e75ade121a9846af81a916e8b1268582&page=5&s=116&click=0
##https://search.jd.com/Search?keyword=%E5%AE%A0%E7%89%A9%E9%9B%B6%E9%A3%9F&qrst=1&wq=%E5%AE%A0%E7%89%A9%E9%9B%B6%E9%A3%9F&stock=1&pvid=e75ade121a9846af81a916e8b1268582&page=7&s=176&click=0

