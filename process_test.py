"""
@author:maohui
@time:2022/5/19 9:31
"""
import time
import multiprocessing

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
    p1=multiprocessing.Process(target=sing)
    p2=multiprocessing.Process(target=dance)
    p1.start()
    p2.start()

if __name__ == "__main__":
    main()
