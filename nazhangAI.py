import requests
# from lxml import etree
import re
import time

url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg5MTM5ODU2Mg==&action=getalbum&album_id=2041739478687416320&scene=173&from_msgid=2247493698&from_itemidx=1&count=3&nolastread=1#wechat_redirect"

# xpath 获取类名里的内容 不方便  弃用
# r = requests.get(url).content.decode()
# print(r.text)
# html = etree.HTML(r)
# result = html.xpath('//ul/li')
# print([i.data-link for i in result])

r = requests.get(url).text

p1 = re.compile(r'data-link="(.*?)"')
p2 = re.compile(r'data-title="(.*?)"')

article_name = re.findall(p2, r)
# for i in re.findall(p2, r):
#     for j in re.findall(p1, r):
#         print(i + ": " + j)
for c,i in enumerate(re.findall(p1, r)):
    # print(requests.get(i).text)
    # print(i)
    abs_path = r'C:\Users\yuyyy\github_pages\secAndintelle\articles\\'

    f = open(abs_path + article_name[c]+ '.html',  'w', encoding='utf-8', errors='ignore') # , encoding='gbk', 
    f.write(requests.get(i).text)
    f.close
    time.sleep(4)