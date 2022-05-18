"""
@author:maohui
@time:2022/5/10 11:37
"""

# 导入socket 库
from socket import *
import pymysql
import datetime




# 1.创建套接字
# 实例化一个socket对象
# 参数 AF_INET 表示该socket网络层使用IP协议（ipv4）
# 参数 SOCK_STREAM 表示该socket传输层使用TCP协议
listenSocket = socket(AF_INET, SOCK_STREAM)

# 2.绑定本地信息blid
# 主机地址为空字符串，表示绑定本机所有网络接口ip地址
# 等待客户端来连接
IP = '192.168.30.43'
# 端口号 9999
PORT = 9999
# 定义一次从socket缓冲区最多读入512个字节数据
BUFLEN = 1
# socket绑定地址和端口
listenSocket.bind((IP, PORT))

# 3.让默认的套接字由主动变为被动listen
# 使socket处于监听状态，等待客户端的连接请求
# 参数 128 表示 最多接受多少个等待连接的客户端
listenSocket.listen(128)
print(f'服务端启动成功，在{PORT}端口等待客户端连接...')

# 5.接收客户端发送过来的请求
# netstat -an|find /i "13333"cmd查看13333端口号服务
# 连接成功的话，有三个，一个是监听，两个是建立连接的客户端和服务端
# global info  # 声明全局变量，将数据传入到flask中
while True:

    # 4.等待客户端的连接
    # 接受客户端的数据,处于堵塞状态
    # (监听套接字负责等待新的客户端进行连接)
    # （accept）产生的新的套接字用来为客户端服务
    dataSocket, client_addr = listenSocket.accept()

    # 连接数据库()
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd="123456", charset='utf8', db='users')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    print('接受一个客户端连接:', client_addr)
    t1 = datetime.datetime.today()# 获取现在时间
    print(t1)
    while True:
        try:
            # 尝试读取对方发送的消息
            # BUFLEN 指定从接收缓冲里最多读取多少字节，默认堵塞
            recved = dataSocket.recv(BUFLEN)
            # 如果返回空bytes，表示对方关闭了连接（客户端调用close那么recv（）就会阻塞）
            # 退出循环，结束消息收发
            if not recved:
                print(f"{client_addr}断开连接")
                break
            # 客户端发送的信息是什么类型的数据，就怎么解码，不一定都是utf8的字符串
            # 读取的字节数据是bytes类型，需要解码为字符串
            info = recved.hex()
        #处理客户端不正常断开
        except ConnectionResetError as e:
            print(f"{client_addr}不正常断开连接")
            break
        #将数据存入数据库
        sql="insert into data(ip,port,data,connect_time) values(%s,%s,%s,%s)"
        cursor.execute(sql,[client_addr[0],client_addr[1],info,t1])
        conn.commit()

        print(f'收到对方信息： {info}')
        # 回收客户端数据
        # 服务器接收到之后，告诉客户端接到了，发送的数据类型必须是bytes，所以要编码
        dataSocket.send(f'服务端接收到了信息 {info}'.encode())
    dataSocket.close()  # 表示关闭为一个客户端的服务，accept（）会继续服务
    cursor.close()
    conn.close()
# 6.关闭套接字
# 服务端也调用close()关闭socket
listenSocket.close()  # 表示关闭一个服务器的服务，accept（）停止服务
