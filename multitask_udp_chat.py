"""
@author:maohui
@time:2022/5/18 16:50
"""
import threading
from socket import *

def recv_msg(udp_socket):
    """接收数据并显示"""
    while True:
        recv_data = udp_socket.recvfrom(1024)
        print(recv_data)

def send_msg(udp_socket,dest_ip,dest_port):
    """发送数据"""
    while True:
        send_data = input(">>>")
        udp_socket.sendto(send_data.encode("utf-8"), (dest_ip, dest_port))

def main():
    """完成udp聊天器的整体控制"""
    # 1.创建套接字
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    # 2.绑定本地信息
    ip = ""
    port = 8888 # 本机调试时，收发数据端口保持不一致
    udp_socket.bind((ip, port))
    # 3.获取对方的ip
    dest_ip = input(">>>ip")
    dest_port = int(input(">>>port"))
    # 4.创建两个线程，去执行相应的功能
    t_recv = threading.Thread(target=recv_msg, args=(udp_socket,))
    t_send = threading.Thread(target=send_msg, args=(udp_socket,dest_ip,dest_port))
    t_recv.start()
    t_send.start()

if __name__ == "__main__":
    main()
