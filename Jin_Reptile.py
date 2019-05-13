import requests

from bs4 import BeautifulSoup

import time
import re

basicUrl = "http://ggzy.guizhou.gov.cn/jygkjsgc/index.jhtml"
# GET /jygkjsgc/index.jhtml HTTP/1.1
# Host: www.gzsggzyjyzx.cn
# Connection: keep-alive
# Pragma: no-cache
# Cache-Control: no-cache
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# Referer: http://www.gzsggzyjyzx.cn/
# Accept-Encoding: gzip, deflate
# Accept-Language: zh-CN,zh;q=0.9
# Cookie: yfx_c_g_u_id_10001141=_ck19041009420810973254483295325; yfx_f_l_v_t_10001141=f_t_1554860527767__r_t_1554860527767__v_t_1554860527767__r_c_0; yfx_mr_10001141=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10001141=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10001141=; JSESSIONID=0205DB3A312CEF00A8B6EA5049477A10; clientlanguage=zh_CN
headerGet = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) chrome/71.0.3578.80 Safari/537.36",
    "Referer": "http://www.gzsggzyjyzx.cn/jyxx/index.jhtml",
    "host": "www.gzsggzyjyzx.cn"
}

headerPost = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    "Referer": "http://www.gzsggzyjyzx.cn/jygkjyjg/index.jhtml",
    "host": "www.gzsggzyjyzx.cn"
}

resFirst = requests.get(basicUrl, headers = headerGet)
    # print(resFirst)
firstSoup = BeautifulSoup(resFirst.text, "lxml")
    # print(firstSoup)

# 处理每页的所有工程详情条目
def soup(postsoup):
    table = postsoup.find(id = "listbox")
    # print(table)
    a_all = table.find_all("a") #变成可遍历的数组
    # print(a_all)
    for a in a_all:
        # print(a['href'])
        a_url = a['href']
        # print(a.text)  工程详情
        engineeringName = a.text
        #解析公司详情页
        detailRes = requests.get(a_url, headers = headerPost)
        
        reg = r'第.中标候选人：[\u4e00-\u9fa5]*|投标报价（元）/下浮率：.*(?=</td>)|项目负责人：[\u4e00-\u9fa5]*'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, detailRes.text)
        # print(imglist)
        # detaulSoup = BeautifulSoup(detailRes.text, "lxml")
        # tbodyList = detaulSoup.find_all('td')    lxml匹配模式 ×××××××××××××××××××××××××××××××××××××
        # # print(tbodyList)
        # firstCandidate = tbodyList[0].text      #第一候选人
        # firstPrice = tbodyList[2].text              #第一候选人报价
        # firstLeader = tbodyList[5].text                 #第一候选负责人
        # secondCandidate = tbodyList[11].text    #第二候选人
        # secondPrice = tbodyList[14].text            #第二候选人报价
        # secondLeader = tbodyList[17].text               #第二候选负责人
        # # thirdCandidate = tbodyList[22].text        #第三候选人
        # # thirdPrice = tbodyList[24].text                 #第三候选人报价
        # # thirdLeader = tbodyList[27].text                    #第三候选负责人
        try:
            firstCandidate = imglist[0]      #第一候选人
            firstPrice = imglist[1]              #第一候选人报价
            firstLeader = imglist[2]                 #第一候选负责人
            secondCandidate = imglist[3]    #第二候选人
            secondPrice = imglist[4]            #第二候选人报价
            secondLeader = imglist[5]               #第二候选负责人
            thirdCandidate = imglist[6]      #第三候选人
            thirdPrice = imglist[7]                 #第三候选人报价
            thirdLeader = imglist[8]            #第二候选负责人
        except:
            continue
        # #测试`````````````````````Success!``
        print(firstCandidate)
        print(firstPrice)
        print(firstLeader)
        print(secondCandidate)
        print(secondPrice)
        print(secondLeader)
        print(thirdCandidate)
        print(thirdPrice)
        print(thirdLeader)
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
    realUrl = "http://www.gzsggzyjyzx.cn/jygkjyjg/index_" + str(page) + ".jhtml"
    # print(realUrl)
    postRes = requests.get(realUrl, headers=headerPost)
    postsoup = BeautifulSoup(postRes.text, "lxml")
    soup(postsoup)