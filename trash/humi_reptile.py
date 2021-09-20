import requests

from bs4 import BeautifulSoup

import time
import re

basicUrl = "http://ggzy.xzsp.tj.gov.cn/jyxxgcjs/index.jhtml"

headerGetIndex = {
    
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
# 目测不需要 "Referer": "ggzy.xzsp.tj.gov.cn/jyxxgcjs/index.jhtmll",
    "host": "ggzy.xzsp.tj.gov.cn"
}

headerGetOthers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    "Referer": "http://ggzy.xzsp.tj.gov.cn/jyxxgcjs/index.jhtml",
    "host": "ggzy.xzsp.tj.gov.cn"
}

# 发送 http 请求到该网站，获得网站内容
firstRes = requests.get(basicUrl, headers = headerGetIndex)
    # print(resFirst)
# 将获得的内容处理为 lxml 的结构,以便使用 lxml 语法拿到所需数据内容 
firstSoup = BeautifulSoup(firstRes.text, "lxml")
    # print(firstSoup)

# 处理每页的所有工程详情条目
def soup(othersoup):
    # 通过检查网页元素发现每一条内容都在 <li> <div class="article-list3-t"> 里
    list_item = othersoup.find(name = 'div',attrs={"class": "article-list3-t"})
    # 通过 find_all方法生成一个元素为 list_item 中所有 a 标签的列表 
    a_all = list_item.find_all('a')
    # 遍历这个列表,取得每一项的 url (网址)
    for a in a_all:
        a_url = a['href']
        # egName = engineeringName(工程项目名称)
        egName = a.text
        print(egName)
# --------------------- 解析工程项目(每个 url)详情页 ------------------------
        detailRes = requests.get(a_url, headers = headerGetOthers)
        print(detailRes.text)
        # reg = r'招标人：[\u4e00-\u9fa5]*|投标报价（元）/下浮率：.*(?=</td>)|项目负责人：[\u4e00-\u9fa5]*'
        # imgre = re.compile(reg)
        # imglist = re.findall(imgre, detailRes.text)
        # try:
        #     firstCandidate = imglist[0]      #第一候选人
        #     firstPrice = imglist[1]              #第一候选人报价
        #     firstLeader = imglist[2]                 #第一候选负责人
        #     secondCandidate = imglist[3]    #第二候选人
        #     secondPrice = imglist[4]            #第二候选人报价
        #     secondLeader = imglist[5]               #第二候选负责人
        #     thirdCandidate = imglist[6]      #第三候选人
        #     thirdPrice = imglist[7]                 #第三候选人报价
        #     thirdLeader = imglist[8]            #第二候选负责人
        # except:
        #     continue
        # # #测试`````````````````````Success!``
        # print(firstCandidate)
        # print(firstPrice)
        # print(firstLeader)
        # print(secondCandidate)
        # print(secondPrice)
        # print(secondLeader)
        # print(thirdCandidate)
        # print(thirdPrice)
        # print(thirdLeader)
# ----------------------------------------------------------
soup(firstSoup)

# 得到总页数
pages_List = firstSoup.find(name="ul", class_="pages-list")
pagesListBar = pages_List.find('a').text
# print(pagesListBar)
totalPage = int(pagesListBar.split('/')[1].split('页')[0])
print("总页数为：--"+str(totalPage))
#  对每页进行处理
for page in range(2, totalPage+1):
    # time.sleep(1) 
    realUrl = "http://ggzy.xzsp.tj.gov.cn/jyxxgcjs//index_" + str(page) + ".jhtml"
    # print(realUrl)
    otherRes = requests.get(realUrl, headers=headerGetOthers)
    otherSoup = BeautifulSoup(otherRes.text, "lxml")
    soup(otherSoup)