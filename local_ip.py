"""
@author:maohui
@time:2022/6/7 12:04
"""
import re
import requests
res = requests.get('http://myip.ipip.net', timeout=1).text
print(res)
ret=re.search(r"[\d]+.*[\d]+",res).group()
print(ret)


import socket
# 函数 gethostname() 返回当前正在执行 Python 的系统主机名
res1 = socket.gethostbyname(socket.gethostname())
print(res1)