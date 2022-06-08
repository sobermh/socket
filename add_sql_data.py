"""
@author:maohui
@time:2022/6/7 10:45
"""
import datetime

import pymysql
from pymysql import cursors
t=0
while t < 1:
    conn = pymysql.connect(host='10.10.10.5', port=3306, user='jqtang', passwd="whcHJKJ*01", charset='utf8', db='whsds')
    cursor = conn.cursor(cursor=cursors.DictCursor)
    t = datetime.datetime.today()
    sql = "insert into sample(type,channel, create_time, update_time, sys_id) values(%s,%s,%s,%s,%s)"
    cursor.execute(sql, [1," ", t, t, 0])
    conn.commit()
    cursor.close()
    conn.close()
    t += 1