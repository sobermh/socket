"""
@author:maohui
@time:2022/5/19 13:13
"""
import os


def main():
    #1.获取用户要copy的文件夹的名字
    old_folder_name=input(">>>")
    #2.创建一个新的文件夹
    os.mkdir(old_folder_name+"附件")
    #3.获取原文件夹中所有待copy的文件名字 listdir（）
    #4.创建进程池
    #5.复制原文件夹中的文件，到新的文件夹中

if __name__=="__main__":
    main()