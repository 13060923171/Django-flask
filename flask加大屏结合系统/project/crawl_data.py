import hashlib
import time  ##调整采集频率
import requests ##发送网络请求
from lxml import etree ##解析html内容
import pprint ##美化输出
import pandas ##导出导入数据等数据存储功能
import os ##路径操作
import json ##json类型和python类型之间的转换


##由于百度贴吧有ip反爬，这里引入熊猫代理-的隧道代理套餐





##定义爬虫类
class CrawlTools(object):


    ##帖子的保存地址
    post_file_path = "post_list.xlsx"
    ##评论的保存地址
    comment_file_path = "comment_list.xlsx"
    ##定义帖子存放的列表
    post_list = []
    ##定义实例化方法：在实例化方法中的操作有：设置请求头参数，创建存放采集数据的临时文件
    def __init__(self) -> None:

        ##设置请求头
        self.headers = {
            "Accept":'*/*',
            "Cookie":'BAIDUID=6A8AD8DB9A88D6A54C81E22F924F7648:FG=1; BAIDUID_BFESS=6A8AD8DB9A88D6A54C81E22F924F7648:FG=1; BAIDU_WISE_UID=wapp_1704871695698_584; USER_JUMP=-1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1703569825,1703576297,1704269382,1704871694; video_bubble0=1; XFI=d11775a0-af89-11ee-889a-7d0745fbf77e; ZFY=vYNs2AtkDvFu2WYXKu6iTxCqY0JbGyp8A8p0QySl8Yc:C; st_key_id=17; arialoadData=false; XFCS=D983D2E4F75F932AD5C6EB2AFE248F577A6DE060254D8BCFFD7AB6224D442007; XFT=kmS0mbiiZbXlXrlTAy4SkecPiHePD5ufilMRnMmMD6M=; wise_device=0; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1704871777; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1704872131; BA_HECTOR=008l842laga001a42ha58l24pkigdj1ipsi631t; Hm_lpvt_287705c8d9e2073d13275b18dbd746dc=1704872132; ab_sr=1.0.1_NGNlNWI4Zjc5MGRlYTNlYjVlMDUwNGM5Y2ExODZmZjA3YzgyNWQ4ODUwZTllNTgzZGUwZjIxYzE2MTI2YmUzM2UzMmExZjFiODNiMDViNTk0NmY1NTM2OTY0ZmEzYmI4M2RlNjY1MDEwNWJlOWE4NTUxOWYxZjg0OGNlNDYzMTQ4Y2RhYmE1ZTU3YTY4MDVjNjE3ZWYxMjQ2NDQ0YWUxZg==; st_data=9f24e43baafbea5a7a826872d0840edf1a10f069e2445fb74755f8a84370d99383e663089d5908301df4e3508faff01654353f91f13c2107826a51d0d124f62fc2787c801514da2ce3254ee9c818633d2c26b9c70c8d018264cfbe786f6522654d3f4f790f1124e01143f9051313ee7fa162b8fc5be176993c3d53af04fd8d618fe1be0e7f40dc8aaf4584232f78b60c; st_sign=6cf5b6f3; RT="z=1&dm=baidu.com&si=bb25547e-8e38-4a30-b445-8b988af459c9&ss=lr7gl5u2&sl=13&tt=njb&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=hn3b&nu=cnn68jhw&cl=hoq8"',
            "Host":'tieba.baidu.com',
            "Referer":'https://tieba.baidu.com/f?kw=%E5%8C%97%E4%BA%AC%E5%86%9C%E5%AD%A6%E9%99%A2&ie=utf-8&pn=0',
            "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        }

        ##如果存放采集临时文件的路径不存在就创建
        if not  os.path.exists("./temp"):
            os.makedirs("./temp")
    
    ##自定义发送网络请求的函数，附带异常捕获
    def send_get_html(self,url,headers,params):
        while 1:
            try:
                ##发送网络请求
                orderno = "DT20230214144701aRwGzkU4"  ##代理ip订单号
                secret = "220fb175b73a1aab382621442594fff3"  ##代理ip账户secret
                ##代理ip转发地址
                ip_port = "dtan.xiongmaodaili.com:8088"

                ##代理ip校验的时间
                timestamp = str(int(time.time()))

                ##代理ip加密体
                txt = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

                ##代理ip加密体进行md5加密
                sign = hashlib.md5(txt.encode()).hexdigest().upper()

                ##将加密体作为认证参数添加到请求头中
                auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp + "&change=true"
                headers["Xiongmao-Proxy-Authorization"] = auth

                ##代理地址
                proxies = {"http": "http://" + ip_port, "https": "http://" + ip_port}
                response = requests.get(
                    url=url,##请求地址
                    headers=headers,##请求头
                    params=params,##请求参数
                    timeout=(4,5),##请求超时时间
                    verify=False,##是否认证
                    proxies=proxies##代理地址
                )

                ##正常请求返回响应
                return response
            except Exception as e:
                ##异常请求：继续请求
                print(f"some error:{e}")
                time.sleep(1)


    ##该函数用来提取html文本里面的纯文本
    def getele(self,text):
        try:
            return etree.HTML(text).xpath("string(.)")
        except:
            return text

    ##该函数是帖子采集的启动函数
    def search_start(self,keyword):



        ##计数器，计数当前页码大小为0的次数
        self.is_zero = 0

        ##遍历页码
        for page in range(1,30):

            ##遍历页码生产帖子的请求地址和请求参数
            url = "https://tieba.baidu.com/mg/f/getFrsData"
            params = {
                "kw": keyword,
                "rn": "100",
                "pn": page,
                "is_good": "0",
                "cid": "0",
                "sort_type": "1",
                "fr": "",
                "default_pro": "1",
                "only_thread_list": "1",
                "eqid": "",
                "refer": "wappass.baidu.com"
            }

            ##调用封装的请求函数，获取响应
            response = self.send_get_html(url,self.headers,params)

            ##获取响应中的帖子列表
            all_post = response.json().get("data",{}).get("thread_list",[])


            ##打印当前列表的大小
            print(f'当前页码大小：',page,len(all_post))


            ##遍历帖子列表，提取，帖子中每一个帖子的数据
            for ipost in all_post:

                try:

                    ##定义字典存放一个帖子的数据：然后按照json取值的方法取如下字段信息：
                    saveitem = {}
                    saveitem["关键字"]= keyword
                    saveitem["帖子id"] = ipost.get("id")
                    saveitem["帖子回复数"] = ipost.get("reply_num")
                    saveitem["帖子点赞数"] = ipost.get("agree",{}).get("agree_num",0)
                    saveitem["帖子反对数"] = ipost.get("agree",{}).get("disagree_num",0)
                    saveitem["帖子标题"] = self.getele(ipost.get("title"))
                    saveitem["作者"] = ipost.get("author",{}).get("name_show")
                    saveitem["作者id"] = ipost.get("author",{}).get("portrait")
                    saveitem["图片"] = "； ".join([i.get("big_pic","") for i in ipost.get("media",[])])
                    saveitem["摘要"] = self.getele(" ".join([i.get("text","") for i in ipost.get("rich_abstract",[])]))
                    saveitem["创建时间"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(ipost.get("create_time")))
                    saveitem["最新回复时间"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(ipost.get("last_time_int")))
                    ##数据保存
                    print(page,len(all_post),saveitem)

                    if ipost.get("create_time") >= time.mktime(time.strptime('2023-08-01','%Y-%m-%d')):
                        self.post_list.append(saveitem)
                except Exception as e:
                    print(f'some error parse error:{e}')
            ##如果当前列表为空，计数器+1 ：这里不直接退出是网站有时候响应空内容，实际上还有下一页：
            if len(all_post) < 1:
                self.is_zero +=1
            
            ##如果持续返回帖子列表为空十次就退出采集
            if self.is_zero > 10:
                break
        

        ##将列表数据转dataframe数据
        df_all = pandas.DataFrame(self.post_list)

        ##通过pandas导出列表数据为excel
        with pandas.ExcelWriter(self.post_file_path,engine='xlsxwriter') as writer:
            df_all.to_excel(writer,index=False)

    ##该函数用来读取-评论函数采集的临时文件转excel
    def get_comment(self):

        ##判断是否有评论采集
        if os.path.exists("./temp/temp.txt"):

            ##如果有采集评论，读取采集的评论
            with open("./temp/temp.txt",'r',encoding='utf-8') as f:
                all_data = [json.loads(i.strip()) for i in f.readlines()]
            
            ##通过pandas导出采集的评论为excel
            df_all = pandas.DataFrame(all_data)
            with pandas.ExcelWriter(self.comment_file_path,engine='xlsxwriter',options={'strings_to_urls': False}) as writer:
                df_all.to_excel(writer,index=False)


    ##该函数是评论采集的入口函数
    def search_comments(self):
        ##判断是否有帖子采集
        start_limit_ = 0
        if os.path.exists(self.post_file_path):

            ##如果有帖子采集，读取采集过的帖子数据
            records = pandas.read_excel(self.post_file_path,dtype=str).to_dict(orient='records')[:]

            ##打印采集的帖子数量
            print(f"总共有帖子数：{len(records)}")


            ##遍历采集的帖子，采集每一个帖子的评论（回复）
            for record_index,irecord in enumerate(records):
                if record_index < start_limit_:
                    continue
                try:
                    print(f"正在访问第：{record_index} 个帖子:{irecord.get('帖子id')}")
                    self.download_detail_comment(irecord)
                
                except Exception as e:
                    print(f'some error:{e}')
            ##导出采集临时文件成excel
            self.get_comment()

    def download_detail_comment(self,irecord):
        if int(irecord.get("帖子回复数")) <=0:
            return
        ##定义帖子回复接口的地址和请求参数
        url = f'https://tieba.baidu.com/mg/p/getPbData'
        params = {
            "kz":irecord.get("帖子id"),
            "obj_param2":'chrome',
            "format":'json',
            "eqid":'',
            "refer":'tieba.baidu.com',
            "pn":1,
            "rn":50,
            "phoneType":2
        }

        ##发送网络请求
        response = self.send_get_html(url,self.headers,params)

        ##获取帖子评论（回复）列表数据
        all_post = response.json().get("data",{}).get("post_list",[])

        print(f"该帖子下有回复：{len(all_post)-1}")

        ##由于第一条回复是帖子本身，这里需要过滤第一条：
        for ipost in all_post[1:]:
            ##读取每一个回复的如下数据
            saveitem = irecord.copy()
            saveitem["评论id"] = ipost.get("id")
            saveitem["评论回复数"] = ipost.get("reply_num")
            saveitem["评论时间"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(ipost.get("time") ))
            saveitem["评论赞同数"] = ipost.get("agree",{}).get("agree_num",0)
            saveitem["评论反对数"] = ipost.get("agree",{}).get("disagree_num",0)
            saveitem["评论者评论"] = ipost.get("author",{}).get("name_show")
            saveitem["评论者id"] = ipost.get("author",{}).get("portrait")
            saveitem["评论文本"] = self.getele(" ".join([i.get("text","") for i in ipost.get("content",[])]))

            print(saveitem)
            ##将每一个回复保存到temp临时我呢见
            with open("./temp/temp.txt",'a',encoding='utf-8') as f:
                f.write(json.dumps(saveitem))
                f.write("\n")

if  __name__ == "__main__":

    ##创建爬虫实例
    tl = CrawlTools()

    ##开始采集帖子
    # tl.search_start('北京大学')
    # tl.search_start('清华大学')
    # tl.search_start('复旦大学')
    # tl.search_start('上海交通大学')
    # tl.search_start('中山大学')

    #开始采集评论（回复）
    tl.search_comments()