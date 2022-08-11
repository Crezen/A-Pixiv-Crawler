# 这是一个示例 Python 脚本。
import os
import re
import ssl
import time
import requests
from urllib.request import urlopen, ProxyHandler, build_opener
from urllib.error import HTTPError
from bs4 import BeautifulSoup
ssl._create_default_https_context = ssl._create_unverified_context


header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77"
}
proxies = {
    "http": "http://47.92.113.71:80",
    "https": "https://211.24.95.49:47615",
}
website = "https://www.tujidao03.com/u/?action=gengxin"
author_id = "22612958"


session = requests.session()
data = {
    "way": "login",
    "username": "18270467851",
    "password": "zdy13694800161"
}

url = "https://www.tujidao03.com/?action=save"
resp = session.post(url, headers=header, data=data)
# print(resp.text)
# print(resp.cookies)

resp1 = session.get("https://www.tujidao03.com/u/?action=gengxin", headers=header)
print(resp1.text)

# response1 = requests.get("https://icanhazip.com/")
# print(response.text)


# 按间距中的绿色按钮以运行脚本。


# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
