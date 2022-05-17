"""
@author:maohui
@time:2022/5/17 10:06
"""

from socket import *

def main():
    #创建一个udp套接字（客户端可以先不绑定端口，系统会随机分）
    udp_socket=socket(AF_INET,SOCK_DGRAM)
    #可以使用套接字持续收发数据
    while True:
        content=input('>>>')#内容
        if content=='exit':
            break
        #!!!内容需要转换为二进制才能发送.encode(“默认utf-8”)//b"xxxx"
        IP='127.0.0.1'#服务器ip
        PORT=3333#端口
        #发送内容和连接服务器的ip和端口
        udp_socket.sendto(content.encode("utf-8"),(IP,PORT))
    #接收服务器的数据,套接字可以同时收发数据
    recv_data=udp_socket.recvfrom(1024)
    print(recv_data)
    #关闭套接字
    udp_socket.close()

if __name__=="__main__":
    main()
