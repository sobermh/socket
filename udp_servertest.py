"""
@author:maohui
@time:2022/5/17 10:36
"""

from socket import *


def main():
    # 1.创建一个套接字
    udp_serversocket = socket(AF_INET, SOCK_DGRAM)
    # 2.绑定ip和端口号(必须是自己电脑的)
    IP = "127.0.0.1"
    PORT = 3333
    udp_serversocket.bind((IP, PORT))
    while True:
        # 3.接受数据
        BUFLEN = 1024  # 每次最多接收多少字节
        recv_data = udp_serversocket.recvfrom(BUFLEN)  # recvfrom接收的数据是元组，(内容,(源ip+port))
        # 4.打印接收的数据
        recv_msg=recv_data[0] #存储接收的数据
        send_addr=str(recv_data[1]) #存储发送方的地址信息
        print(f'{send_addr}:{recv_msg.decode()}')
        print(recv_data)
    # 5.关闭套接字
    udp_serversocket.close()

if __name__ == "__main__":
    main()
