from concurrent import futures
from tqdm import tqdm
import openpyxl
import requests
from bs4 import BeautifulSoup


wb = openpyxl.Workbook()  # 创建一个Excel表
s = wb.active
s.title = '微博数据'
s['A1'] = '关键词'
s['B1'] = '用户名称'
s['C1'] = '发布时间'
s['D1'] = '发布内容'
s['E1'] = '转发数'
s['F1'] = '评论数'
s['G1'] = '点赞数'
s['H1'] = '关注数'
s['I1'] = '粉丝数'
s['J1'] = '用户等级'
s['K1'] = '发博总数'
s['L1'] = '认证'
s['M1'] = '用户地址'
s['N1'] = '会员类型'
s['O1'] = '生日'
s['P1'] = '毕业院校'

def acquire_data(words):
    for i in range(1, 2):#因为微博最多只能50页
        url = f'https://s.weibo.com/weibo?q={words[0]}&typeall=1&suball=1&timescope=custom:{words[1]}-0:{words[1]}-23&Refer=g&page={i}'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'SINAGLOBAL=2709944481384.8584.1657871763039; UOR=,,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5GwlB4mf13pUNVQ0MzU9ZV5JpX5KMhUgL.Fo-0eK.01hBfehe2dJLoIEBLxKqL1-eL1h.LxKML12eLB-zLxKnL1h-LB.zLxK-LBKqL1Kqt; ULV=1663897424619:8:3:2:1974743960182.8054.1663897424523:1663663928945; PC_TOKEN=8109017931; ALF=1698306948; SSOLoginState=1666770952; SCF=Arxx7kQrC3-n8rahVXFqs2qLu3V3RA4xu8ep7P9Nmzu89UpZHDHg4CejlKtSiDM8Es9Q-0sFVkTE7MhC61cZvBo.; SUB=_2A25OXJhaDeRhGeNN6lsS-CrJyz-IHXVtK46SrDV8PUNbmtAfLXnHkW9NSdnQVBeTQ-Jh9YOX2FEq1DujgOeheE-q; wvr=6',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        }#请求头
        # sleep(1)
        # print('1秒后继续采集')
        ss = requests.session()
        ss.keep_alive = False#把会话保存成一个对象
        while 1:
            try:
                html0 = ss.get(url=url, headers=headers).text#对目标网站发起请求
                break
            except:
                pass
        t = BeautifulSoup(html0, 'lxml')#实例化获取到的信息

        card = t.find_all('div', class_="card-wrap")

        try:
            pd = t.find('img', class_="no-result")['src']
            if pd=='https://simg.s.weibo.com/20211124_noresult.png':
                break
        except:
            pd=''
        for p in card:
            try:
                te=p.find_all('p', class_="txt")

                txt = str(p.find_all('p', class_="txt")[-1].text).replace('\n', '').replace('\u200b','').replace('收起d','').replace(' ', '')#获取博文内容
                pl = str(p.find_all('a', class_="woo-box-flex woo-box-alignCenter woo-box-justifyCenter")[-2].text).replace(' ','')#获取评论量
                name = p.find('a', class_="name").text#获取发博人的名称

                time = str(p.find('div', class_="from").a.text).replace(' ', '').replace('\n', '').replace('\xa0','')#获取发博时间

                ti = time.split('来自')[0]
                dz = str(p.find_all('span', class_="woo-like-count")[-1].text).replace(' ', '')#获取点赞量
                zf = str(p.find_all('a', class_="woo-box-flex woo-box-alignCenter woo-box-justifyCenter")[-3].text).replace(' ', '')#获取转发量
                if dz == '赞':
                    dz = 0
                if zf == '转发':
                    zf = 0
                if pl == '评论':#把他们变成数字
                    pl = 0
                mid=p['mid']
                bzid=str(p.find('div',class_="avator").a['href']).split('?')[0].split('/')[-1]
                uuuu = f'https://weibo.com/ajax/profile/info?custom={bzid}'
                while 1:
                    try:
                        uuuht = requests.get(url=uuuu, headers=headers).json()
                        break
                    except:
                        pass
                uid = uuuht['data']['user']['id']
                yhurl = f'https://weibo.com/ajax/profile/info?uid={uid}'  # 用户url
                while 1:
                    try:
                        uhht = requests.get(url=yhurl, headers=headers).json()
                        break
                    except:
                        pass
                try:
                    gzs = uhht['data']['user']['friends_count']  # 关注数
                except:
                    gzs = ''
                fss = uhht['data']['user']['followers_count_str']  # 粉丝数
                hydj = uhht['data']['user']['mbrank']  # 等级
                fbzs = uhht['data']['user']['statuses_count']  # 发博总数
                try:
                    rz = uhht['data']['user']['verified_reason']  # 认证
                except:
                    rz = ''
                yhdz = 'https://weibo.com' + uhht['data']['user']['profile_url']  # 用户地址
                try:  # 下边一段内容是获取用户会员类型
                    A = uhht['data']['user']['verified_type']
                    T = uhht['data']['user']['verified_type_ext']

                    if uhht['data']['user']['verified']:
                        if A == 0:
                            if T == 1:
                                YH = '金v'
                            else:
                                YH = '黄v'

                        if 0 < A < 8:
                            if A == 2 and t == -1:
                                YH = '蓝v'
                            else:
                                YH = '蓝v'
                    else:
                        YH = '普通用户'
                except:
                    YH = '普通用户'
                uuuul=f'https://weibo.com/ajax/profile/detail?uid={uid}'
                while 1:
                    try:
                        uuhe=requests.get(url=uuuul,headers=headers).json()
                        break
                    except:
                        pass
                try:
                    sr=uuhe['data']['birthday']
                except:
                    sr=''
                try:
                    bye=uuhe['data']['education']['school']
                except:
                    bye=''
                yhdata = [gzs, fss, hydj, fbzs, rz, yhdz, YH,sr,bye]  # 保存成列表方便保存

                data=[words[0],name,ti,txt,zf,pl,dz]+yhdata#吧获取到的数据存进列表
                s.append(data)  # 吧data保存到表格里
                return '成功写入'
                # print('成功写入', data)
            except:
                return '写入失败'
    wb.save(f'./demo/data/微博数据1.xlsx')  # 保存数据


# if __name__ == '__main__':
#     word_data=[]
#     import datetime
#     dic={
#         '莫兰蒂':['2016-09-10','2016-09-18'],
#         '灿都':['2021-09-07','2021-09-20'],
#         '马鞍':['2022-08-22','2022-08-28'],
#         '梅花':['2022-09-08','2022-09-18']
#
#     }
#     for wor in tqdm(dic.keys()):
#         for ti in dic.values():
#             k =ti[0]
#             j =ti[1]  # 设置范围
#             dates = []
#             dt = datetime.datetime.strptime(k, "%Y-%m-%d")
#             date = k[:]
#             while date <= j:
#                 dates.append(date)
#                 dt = dt + datetime.timedelta(1)
#                 date = dt.strftime("%Y-%m-%d")
#             for tii in dates:  # 循环这一年的每天
#                 words=[wor,tii]
#                 acquire_data(words)
