"""
@author:maohui
@time:2022/5/10 11:49
"""
import time
from socket import *


#1.创建tcp套接字
# 实例化一个socket对象，指明协议，ip/tcp
tcpc_Socket = socket(AF_INET, SOCK_STREAM)

#2.链接服务器
#服务端ip和端口
# IP = '192.168.30.43'
IP = gethostbyname(gethostname())
SERVER_PORT = 9999
BUFLEN = 1024


# #####客户端绑定
# ip1='192.168.30.43'
# client_port=56023
# tcpc_Socket.bind((ip1,client_port))


# 连接服务端socket
tcpc_Socket.connect((IP, SERVER_PORT))

print(1)
#3.发送数据
while True:
    # 从终端读入用户输入的字符串
    # toSend =input('>>> ')
    # if  toSend =='exit':
    #     break
    # 发送消息，也要编码为 bytes

    tcpc_Socket.send('111111111111111111111111111111111111111111111112'.encode('ascii'))
    time.sleep(0.5)
    print(1)
    # 等待接收服务端的消息
    # recved = tcpc_Socket.recv(BUFLEN)
    # #ewqe 如果返回空bytes，表示对方关闭了连接
    # if not recved:
    #     break
    # # # 打印读取的信息
    # print(recved.decode())

#4.关闭套接字
tcpc_Socket.close()