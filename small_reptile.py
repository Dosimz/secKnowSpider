import requests
from bs4 import BeautifulSoup
import re

base_url = "http://www.qnggzy.cn/TPWeb_QN/gcjs/009002/"
headerGet = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) chrome/71.0.3578.80 Safari/537.36",
    "Referer" : "http://www.qnggzy.cn/TPWeb_QN/",
    "host" : "www.qnggzy.cn",
}

def get_html_parse():
    result_get = requests.get(base_url, headers = headerGet)
    soup = BeautifulSoup(result_get.text, "lxml")
    return soup

def do_html_papers(html_parse):
    a_list = html_parse.find_all("a", target = "_blank")
    # print(a_list)
    for a in a_list: 
        a_url = 'http://www.qnggzy.cn' + a['href']
        print(a_url)
        a_name = a.text
        a_detail = requests.get(a_url, headers = headerGet)
        # print(a_detail.text)
        # regC = r'[\u4e00-\u9fa5]*有限公司'
        # info_reC = re.compile(regC)
        # info_listC = re.findall(info_reC, a_detail.text)
        # print("第一中标候选人" + info_listC[-3])
        # print("第二中标候选人" + info_listC[-2])
        # print("第三中标候选人" + info_listC[-1])
        # regF = r'^[\u4E00-\u9FA5]{2,4}$'
        # info_reF = re.compile(regF)
        # info_listF = re.findall(info_reF, a_detail.text)
        # print(info_listF)
        
do_html_papers(get_html_parse())