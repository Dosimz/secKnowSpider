import requests

from bs4 import BeautifulSoup

import time
import re

basicUrl = "http://220.163.15.148/InfoQuery/PersonnelList"

headerGetIndex = {
    
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
# 目测不需要 "Referer": "ggzy.xzsp.tj.gov.cn/jyxxgcjs/index.jhtmll",
    "host": "220.163.15.148"
}

headerGetOthers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    "Referer": "http://220.163.15.148/InfoQuery/PersonnelList?page=1",
    "host": "220.163.15.148"
}

# 发送 http 请求到该网站，获得网站内容
firstRes = requests.get(basicUrl, headers = headerGetIndex)
    # print(resFirst)
# 将获得的内容处理为 lxml 的结构,以便使用 lxml 语法拿到所需数据内容 
firstSoup = BeautifulSoup(firstRes.text, "lxml")
    # print(firstSoup)

# 处理每页的所有工程详情条目
def soup(othersoup):
    trs = firstSoup.select('tr')
    i = 1
    for tr in trs:
        name = firstSoup.select('#Name' + str(i) + '> a')
        print(name)
        a = tr.select('tr > td:nth-child(4)')
        print(a)
        b = tr.select('tr > td:nth-child(5)')
        print(b)
        c = tr.select('tr > td:nth-child(6)')
        print(c)
        i += 1
# --------------------------------------------------------------

#---------------------- # 通过检查网页元素发现每一条内容都在 tbody 里------------------
    # list_item = othersoup.find('tbody')
    # # print(list_item)
    # res = firstSoup.tbody.children
    # print(res)
    # for tr in res:
    #     td_all = tr.find_all('')
#-----------------------------------     print(td_all) ---------------------
soup(firstSoup)

# 求总页数
pages_List = firstSoup.select('div.jump.fl > span:nth-child(1)')
# pagesListBar = pages_List.find('a').text
total = str(pages_List[0])
# totalPage = int(pages_List[0].split('共')[1].split('条')[0])
reg = r'(\d{5})'
imgre = re.compile(reg)
imglist = re.findall(imgre, total) # 得到 ['77402']
# print(int(imglist[0]))   得到 int 类型的 77402 
#  对每页进行处理
pages = int(imglist[0]) // 15  # 页数 = 77402 条 // 每页 15 条
for page in range(2, pages+1):
#     # time.sleep(1) 
    realUrl = "http://220.163.15.148/InfoQuery/PersonnelList?page=" + str(page)
#     # print(realUrl)
    otherRes = requests.get(realUrl, headers=headerGetOthers)
    otherSoup = BeautifulSoup(otherRes.text, "lxml")
    soup(otherSoup)