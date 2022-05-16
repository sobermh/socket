"""
@author:maohui
@time:2022/5/10 11:37
"""

#  === TCP 服务端程序 tcp_server.py ===

# 导入socket 库
from socket import *

# 主机地址为空字符串，表示绑定本机所有网络接口ip地址
# 等待客户端来连接
IP = '0.0.0.0'
# 端口号 9999
PORT = 13333
# 定义一次从socket缓冲区最多读入512个字节数据
BUFLEN = 512

# 实例化一个socket对象
# 参数 AF_INET 表示该socket网络层使用IP协议（ipv4）
# 参数 SOCK_STREAM 表示该socket传输层使用TCP协议
listenSocket = socket(AF_INET, SOCK_STREAM)

# socket绑定地址和端口
listenSocket.bind((IP, PORT))

# 使socket处于监听状态，等待客户端的连接请求
# 参数 8 表示 最多接受多少个等待连接的客户端,处于睡眠状态
listenSocket.listen(8)
print(f'服务端启动成功，在{PORT}端口等待客户端连接...')

#接受客户端的数据
dataSocket, addr = listenSocket.accept()
print('接受一个客户端连接:', addr)

#netstat -an|find /i "13333"cmd查看13333端口号服务
# 连接成功的话，有三个，一个是监听，两个是建立连接的客户端和服务端
global info # 声明全局变量，将数据传入到flask中
while True:
    # 尝试读取对方发送的消息
    # BUFLEN 指定从接收缓冲里最多读取多少字节
    recved = dataSocket.recv(BUFLEN)

    # 如果返回空bytes，表示对方关闭了连接
    # 退出循环，结束消息收发
    if not recved:
        break

    # 客户端发送的信息是什么类型的数据，就怎么解码，不一定都是utf8的字符串
    # 读取的字节数据是bytes类型，需要解码为字符串

    info = recved.decode()
    print(f'收到对方信息： {info}')

    # 服务器接收到之后，告诉客户端接到了，发送的数据类型必须是bytes，所以要编码
    dataSocket.send(f'服务端接收到了信息 {info}'.encode())

# 服务端也调用close()关闭socket
dataSocket.close()
listenSocket.close()