"""
@author:maohui
@time:2022/5/10 11:49
"""


from socket import *


#1.创建tcp套接字
# 实例化一个socket对象，指明协议，ip/tcp
tcp_Socket = socket(AF_INET, SOCK_STREAM)

#2.链接服务器
#服务端ip和端口
IP = '127.0.0.1'
SERVER_PORT = 3333
BUFLEN = 1024
# 连接服务端socket
tcp_Socket.connect((IP, SERVER_PORT))

#3.发送数据
while True:
    # 从终端读入用户输入的字符串
    toSend = input('>>> ')
    if  toSend =='exit':
        break
    # 发送消息，也要编码为 bytes
    tcp_Socket.send(toSend.encode())
    # 等待接收服务端的消息
    recved = tcp_Socket.recv(BUFLEN)
    # 如果返回空bytes，表示对方关闭了连接
    if not recved:
        break
    # # 打印读取的信息
    print(recved.decode())

#4.关闭套接字
tcp_Socket.close()