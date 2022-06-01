"""
@author:maohui
@time:2022/5/27 14:23
"""

import re

print(re.match(r"\d{1}", "1").group())

html_content = """fdsf
dsa
d
asd
das
da
das"""
print(re.match(r".*",html_content,re.S).group())
def main():
    names=["name1","_name","2_name","name!"]
    for name in names:
        ret=re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$",name)
        if ret:
            print("%s"%name)
        else:
            print("false")
def main1():
    email=input(">>>")##邮箱地址
    #如果在正则表达式中需要用到某些特殊的字符，如：. ? 等，需要在他们前面添加一个反斜杠进行转义
    ret=re.match(r"^[a-zA-Z_0-9]{4,20}@163\.com$",email)
    if ret:
        print("%s符合要求"%email)
    else:
        print("%s不符合要求" % email)
if __name__=="__main__":
    main()
    main1()