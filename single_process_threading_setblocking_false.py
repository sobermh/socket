"""
@author:maohui
@time:2022/6/2 9:17
"""

from socket import *

tcp_server=socket(AF_INET,SOCK_STREAM)
tcp_server.bind(("",7899))
tcp_server.listen(128)
tcp_server.setblocking(False)

client_socket_list=list()

while True:
    try:
        new_socket,new_addr=tcp_server.accept()
    except Exception as e:
        print("没有新的客户端到到来")
    else:
        print("到来一个新的客户端")
        new_socket.setblocking(False)
        client_socket_list.append(new_socket)

    for client_socket in client_socket_list:
        try:
            recv_data=client_socket.recv(1024)
        except Exception as e:
            print(e)
            print("没有收到数据")
        else:
            print(recv_data)
            if recv_data:
                print("客户端发来了数据")
            else :
                client_socket.close()
                client_socket_list.remove(client_socket)