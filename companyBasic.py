# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:40:48 2019
贵州省住建厅 公共信息平台 （企业基本信息，资质信息）
@author: 86158
"""
import requests

from bs4 import BeautifulSoup

import time
import re

from pymongo import MongoClient
# 开启mongo客户端
conn = MongoClient("127.0.0.1", 27017)
# 连接数据库
db = conn.get_database('guizhou')
# 连接集合
my_table = db.get_collection("company")


# 处理一页的数据
def soup(postsoup):
    table = postsoup.find(id="DG_List")

    tr_all = table.find_all('tr')

    for tr in tr_all:

        td_all = tr.find_all('td')

        if td_all[0].text.isdigit():
            time.sleep(1)
            companyName = td_all[1].text

            a_url = "http://220.197.219.123:88/Web/dataapp/" + \
                td_all[1].a['href']

            detailRes = requests.get(a_url, headers=headerPost)

            detaulSoup = BeautifulSoup(detailRes.text, "lxml")

            detailTable = detaulSoup.find(id="entBaseInfo")

            tr_all = detailTable.find_all('tr')
            # 企业名称
            companyName = tr_all[0].find_all('td')[1].text.replace(
                "\n", "").replace("\t", "").replace(" ", "").replace("\r", "")
            # 企业类型
            type_ = tr_all[0].find_all('td')[3].text.replace(
                "\n", "").replace("\t", "").replace(" ", "").replace("\r", "")
            # 企业所在地
            location = tr_all[1].find_all('td')[1].text.replace(
                "\n", "").replace("\t", "").replace(" ", "").replace("\r", "")
            # 详细地址
            detailAddress = tr_all[1].find_all('td')[3].text.replace(
                "\n", "").replace("\t", "").replace(" ", "").replace("\r", "")
            # 邮政编码
            poscode = tr_all[2].find_all('td')[1].text.replace(
                "\n", "").replace("\t", "").replace(" ", "").replace("\r", "")
            # 联系电话
            phoneNum = tr_all[2].find_all('td')[3].text.replace(
                "\n", "").replace("\t", "").replace(" ", "").replace("\r", "")
            # 资质证书编号
            cerificateNum = tr_all[3].find_all('td')[1].text.replace(
                "\n", "").replace("\t", "").replace(" ", "").replace("\r", "")
            # 有效期至
            validtyDate = tr_all[3].find_all('td')[3].text.replace(
                "\n", "").replace("\t", "").replace(" ", "").replace("\r", "")

            print("企业名称---"+companyName+"\n")
            print("企业类型---"+type_+"\n")
            print("企业所在地---"+location+"\n")
            print("详细地址---"+detailAddress+"\n")
            print("邮政编码---"+poscode+"\n")
            print("联系电话---"+phoneNum+"\n")
            print("资质证书编号---"+cerificateNum+"\n")
            print("有效期至---"+validtyDate+"\n")

            # 公司基本数据数据库存入准备`````
            comPanyBasic = {"companyName": companyName, "type_": type_, "location": location,
                            "detailAddress": detailAddress, "poscode": poscode, "phoneNum": phoneNum,
                            "cerificateNum": cerificateNum, "validtyDate": validtyDate}

            # 资质表格
            qualTable = detaulSoup.find(id="DG_List")
            # 资质项
            qualTrall = qualTable.find_all(name="tr", class_="bdhvor")

            qualList = []

            for tr in qualTrall:
                td_all = tr.find_all("td")
                # 证书编号
                cernumber = td_all[1].text
                # 资质等级
                quallevel = td_all[2].text
                # 资质名称
                qualname = td_all[3].text
                # 资质类别
                qualType = td_all[4].text

                qualOnemap = {"cernumber": cernumber, "quallevel": quallevel,
                              "qualname": qualname, "qualType": qualType}

                qualList.append(qualOnemap)

            comBasic = {"companyBasic": comPanyBasic, "qualList": qualList}

            print(comBasic)

            # 将数据添加到数据库中.................................................................
            if my_table.find_one({"companyBasic.companyName": companyName}):
                print("不用添加该条数据")
            else:
                my_table.insert(comBasic)


basicUrl = "http://220.197.219.123:88/Web/dataapp/ent_dataResult.aspx"

# 伪装成浏览器
headerGet = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
             "Referer": "http://220.197.219.123:88/",
             "host": "220.197.219.123:88"}
headerPost = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
              "Referer": "http://220.197.219.123:88/Web/dataapp/ent_dataResult.aspx",
              "host": "220.197.219.123:88"}


resFirst = requests.get(basicUrl, headers=headerGet)

firstSoup = BeautifulSoup(resFirst.text, "lxml")


soup(firstSoup)

# 得到总页数
pageHtml = firstSoup.find(name="td", class_="pagescount").text
totalPage = int(pageHtml.split('/')[1].split('页')[0])
print("总页数为：--"+str(totalPage))

__VIEWSTATE = firstSoup.find(id="__VIEWSTATE")['value']


for page in range(2, totalPage+1):
    print("请求第"+str(page)+"页")
    condition = {"__VIEWSTATE": __VIEWSTATE, "__VIEWSTATEGENERATOR": "B210BEA4",
                 "__EVENTTARGET": "Pager1", "__EVENTARGUMENT": str(page), "t_FSystemId": '101', }
    postRes = requests.post(basicUrl, headers=headerPost, data=condition)

    postsoup = BeautifulSoup(postRes.text, "lxml")

    soup(postsoup)

    __VIEWSTATE = postsoup.find(id="__VIEWSTATE")['value']
