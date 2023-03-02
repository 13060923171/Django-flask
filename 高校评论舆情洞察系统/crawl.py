import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import time
import random
from tqdm import tqdm
import pandas as pd
from urllib import parse


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

with open('./data/cookie.txt','r') as f:
    cookie = f.read().strip('\n')

headers = {
    "Host": "tieba.baidu.com",
    "User-Agent": random.choice(user_agent),
    'Cookie': '{}'.format(cookie)
}

session = requests.session()


#检查是否反应正确
def get_parse(url):
    html = session.get(url,headers=headers)
    if html.status_code ==200:
        print(html.status_code)
        get_html(html)
    else:
        print(html.status_code)


#获取每一页的贴吧的URL
def get_html(html):
    content = html.text
    daihao = re.compile("data-tid='(.*?)'",re.S|re.I)
    result = daihao.findall(content)
    for i in result:
        get_page(i)

#获取每一个贴里面的页数
def get_page(i):
    url = "https://tieba.baidu.com/p/" + i
    r = session.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    try:
        #用BeautifulSoup去获取每一个贴里面有多少页
        span = soup.find_all('span',class_ = 'red')
        tiebayeshu = str(span[1]).replace('<span class="red">', '').replace('</span>', '')
        get_pinglin(i, tiebayeshu)
    except:
        pass

#获取贴吧里面评论的页数的URL
def get_pinglin(i,yeshu):
    list = []
    for j in range(1, int(yeshu) + 1):
        url = "https://tieba.baidu.com/p/{}?pn={}".format(i,j)
        list.append(url)
        get_neirong(list)

#获取每一个URL里面的评论内容
def get_neirong(list):
    #传入列表里面的URL
    for i in list:
        r = session.get(i,headers=headers)
        soup = etree.HTML(r.text)
        content = soup.xpath('//div[@class="d_post_content j_d_post_content  clearfix"]/text()')
        date_time = re.compile("&quot;(\d+\-\d+-\d+.*\d+\:\d+)&quot;")
        date_time1 = date_time.findall(r.text)
        df = pd.DataFrame()
        df['内容'] = content
        df['时间'] = date_time1
        df.to_csv('./data/data.csv', encoding='utf-8-sig', index=False, header=False, mode='a+')
    time.sleep(random.random())


def main1():
    data = pd.read_csv('./data/data.csv')
    data = data.drop_duplicates(keep='first')
    data = data.dropna(how='any',axis=0)
    def main1(x):
        x1 = str(x).strip(' ')
        return x1
    data['内容'] = data['内容'].apply(main1)
    data.to_csv('./data/{}.csv'.format(word), encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    word = '郑州大学'
    df = pd.DataFrame()
    df['内容'] = ['内容']
    df['时间'] = ['时间']
    df.to_csv('./data/data.csv',encoding='utf-8-sig',index=False,header=False,mode='w')
    keyword = parse.quote(word)
    #页数
    number_page = 20
    #50为一页
    for i in tqdm(range(0,int(number_page * 50)+1,50)):
        url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}".format(keyword,i)
        get_parse(url)
    main1()