"""
@author:maohui
@time:2022/5/17 15:07
"""

import time
import threading


def sing():
    """唱歌5秒钟"""
    for i in range(5):
        print("---正在唱---")
        time.sleep(1)


def dance():
    """跳舞5秒钟"""
    for i in range(5):
        print("---dance---")
        time.sleep(1)




def main():
    #创建实例对象
    t1 = threading.Thread(target=sing)
    t2 = threading.Thread(target=dance)
    t1.start()#创建了线程，并启动线程,开始执行
    t2.start()
    while True:
        length=len(threading.enumerate())
        print('当前运行的线程数为：%d'%length)
        if length<=1:
            break


if __name__ == "__main__":
    main()
