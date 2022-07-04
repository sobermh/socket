"""
@author:maohui
@time:2022/5/10 11:37
"""

# 导入socket 库
import os
import re
import socket
import time
import zipfile
from threading import Thread
from socket import *
import pymysql
import datetime
from smtplib import SMTP_SSL  # 加密及发送邮件内容
from email.mime.application import MIMEApplication  # 添加附件
from email.mime.multipart import MIMEMultipart  # 邮件的主体
from pymysql import cursors


def R_chx(chx,rx):
    """对socket接收到的数据进行公式计算分析，ADC输出的数据和芯片分压的对应关系"""
    voltage_data=1.65 + (chx * 3.0 / 65535 - 1.65) / 2.8
    # 芯片电阻和芯片分压的对应关系
    chx_r = (3.3 - voltage_data) * rx / voltage_data
    # round(chx_r, 2)保留两位小数位
    # 保留八位有效位数
    return float(format(chx_r, '.8g'))

# 1.创建套接字
# 实例化一个socket对象
# 参数 AF_INET 表示该socket网络层使用IP协议（ipv4）
# 参数 SOCK_STREAM 表示该socket传输层使用TCP协议
listenSocket = socket(AF_INET, SOCK_STREAM)

listenSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, True)
listenSocket.ioctl(SIO_KEEPALIVE_VALS, (1, 3600 * 1000, 1800 * 1000))

# 2.绑定本地信息blid
# 主机地址为空字符串，表示绑定本机所有网络接口ip地址
# 等待客户端来连接
IP = gethostbyname(gethostname())
# IP = "192.168.3.26"
# 端口号 9999
PORT = 9999
# 定义一次从socket缓冲区最多读入512个字节数据
BUFLEN = 58
# socket绑定地址和端口
listenSocket.bind((IP, PORT))

# 3.让默认的套接字由主动变为被动listen
# 使socket处于监听状态，等待客户端的连接请求
# 参数 128 表示 最多接受多少个等待连接的客户端
listenSocket.listen(128)
print(f'服务端启动成功，在{PORT}端口等待客户端连接...')

def zip_file(file_create_time):
    """压缩文件夹，生成新的压缩文件"""
    file_name=str(file_create_time)
    start_dir = f'c:/data/{file_name}' # 要压缩的文件夹路径
    file_news = start_dir + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        f_path = dir_path.replace(start_dir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        f_path = f_path and f_path + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), f_path + filename)
    z.close()
    return file_news

file_create_time=datetime.date.today() # 没有时分秒
# file_create_time = datetime.datetime.today()  # 完整时间
folder_path=""
def create_file_time(file_create_time,folder_path):
    """5天创建一个文件夹"""
    while True:
        try:
            file_name=str(file_create_time)
            folder_path = f'c:/data/{file_name}'
            os.makedirs(folder_path)
            # 5天
            time.sleep(432000)
            file_create_time = datetime.datetime.today()
        except Exception as e:
            t_error = datetime.datetime.today()  # 获取现在时间
            with open("./log.txt", "w") as f:
                f.write(f"time={t_error},e={e},---------------------")
            time.sleep(86400)


def data_send_email(file_create_time):
    """5天一次,将数据发生到指定邮箱"""
    #发送人
    while True:
        from_addr="maohui@well-healthcare.com"
        with open("./python-authcodes.txt",mode='r',encoding="utf-8") as file:
            authcodes=file.read()
        print(authcodes)
        # 输入SMTP服务器地址
        smtp_server = "smtp.exmail.qq.com"
        #收件人，
        to_addr="nipengyun@well-healthcare.com"
        #附件,添加一个头部使发送的不为.bin
        fujian=MIMEApplication(open(zip_file(file_create_time),'rb').read())
        fujian.add_header('Content-Disposition', 'attachment', filename=re.search(r"[\d]+.*",zip_file(file_create_time)).group())
        print(re.search(r"[\d]+.*",zip_file(file_create_time)).group())
        #初始化邮件
        msg=MIMEMultipart()#初始化主体
        msg['Subject'] = re.search(r"[\d]+.*",zip_file(file_create_time)).group() # 放入标题
        msg.attach(fujian) #放入附件
        #发送
        smtp=SMTP_SSL(smtp_server,465) # 连接发送的邮箱服务器
        smtp.login(from_addr,authcodes)# 登录发送的邮箱
        smtp.sendmail(from_addr, to_addr, msg.as_string())
        #5天
        time.sleep(432000)
def sql_to_excel(file_create_time):
        """一周导出一次数据库数据，并清空数据库,重新赋值时间戳，发送至邮箱。。。"""
        # 设置时间线，以其为标准，对数据库进行导出清空
        while True:
            try:
                # t_server_begin = datetime.datetime.today()
                # t_server_begin1=datetime.date.today()-datetime.timedelta(days=3)
                t_server_begin = datetime.date.today()  # 获取当前没有时间的日期
                conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd="123456", charset='utf8', db='users')
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                file_name=str(file_create_time)
                print(file_name)
                print(f'c:/data/{file_name}/{t_server_begin}.xls')
                sql = f"select * from data into outfile 'c:/data/{file_name}/{t_server_begin}.xls'"
                # f"select * from data into outfile 'c:/data/{t_server_begin}.xlsx'"
                cursor.execute(sql,)
                conn.commit()
                sql = "truncate table data"
                cursor.execute(sql,)
                conn.commit()
                # #调用发送邮件函数发送,office的xls
                # file_path=folder_path+'/'+str(t_server_begin)+'.xls'
                # data_send_email(file_path)
                #一天
                time.sleep(86400)
            except Exception as e:
                t_error = datetime.datetime.today()  # 获取现在时间
                with open("./log.txt", "w") as f:
                    f.write(f"time={t_error},e={e}")
                print(e)
                time.sleep(86400)
# 5.接收客户端发送过来的请求
# netstat -an|find /i "13333"cmd查看13333端口号服务
# 连接成功的话，有三个，一个是监听，两个是建立连接的客户端和服务端
# global info  # 声明全局变量，将数据传入到flask中
def clientHandler(dataSocket,client_addr):
    """socket服务器"""
    while True:
            # 连接数据库()
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd="123456", charset='utf8', db='users')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            t1 = datetime.datetime.today()# 获取现在时间
            print(t1)
            count=1
            while True:
                # try:
                # 尝试读取对方发送的消息
                # BUFLEN 指定从接收缓冲里最多读取多少字节，默认堵塞
                dataSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, True)
                dataSocket.ioctl(SIO_KEEPALIVE_VALS, (1, 3600* 1000, 1800 * 1000))
                try:
                    recved = dataSocket.recv(BUFLEN)
                    t2=datetime.datetime.today()
                    ###记录第一次接收到连接数据的时间
                    # if count==1:
                    #     sql = "insert into status(status,ip,port,connect_time) values(%s,%s,%s,%s)"
                    #     cursor.execute(sql, ["接收到连接数据",client_addr[0],client_addr[1],t2])
                    #     conn.commit()
                    # count+=1
                    # # 如果返回空bytes，表示对方关闭了连接（客户端调用close那么recv（）就会阻塞）
                    # 退出循环，结束消息收发
                    if not recved:
                        t_close = datetime.datetime.today()
                        # sql = "insert into status(status,ip,port,close_time) values(%s,%s,%s,%s)"
                        # cursor.execute(sql, ["客户端断开连接", client_addr[0], client_addr[1], t_close])
                        print(f"{client_addr}断开连接")
                        break
                    # 客户端发送的信息是什么类型的数据，就怎么解码，不一定都是utf8的字符串
                    # 读取的字节数据是bytes类型，需要解码为字符串,2->10->16
                    info = recved#解码，去除b’‘
                    print(f'收到对方信息： {info}')
                    #包左不包右
                    CH1 =info[2:4]
                    #bytes转化为int
                    ch1_int=int.from_bytes(CH1, byteorder='big', signed=False)
                    r1 =info[18:22]
                    r1_int=int.from_bytes(r1, byteorder='big', signed=False)
                    ch1_r1 = R_chx(ch1_int,r1_int)

                    CH2 =info[4:6]
                    ch2_int = int.from_bytes(CH2, byteorder='big', signed=False)
                    r2 = info[22:26]
                    r2_int = int.from_bytes(r2, byteorder='big', signed=False)
                    ch2_r2 = R_chx(ch2_int,r2_int)

                    CH3 =info[6:8]
                    ch3_int = int.from_bytes(CH3, byteorder='big', signed=False)
                    r3 = info[26:30]
                    r3_int = int.from_bytes(r3, byteorder='big', signed=False)
                    ch3_r3 = R_chx(ch3_int,r3_int)

                    CH4 =info[8:10]
                    ch4_int = int.from_bytes(CH4, byteorder='big', signed=False)
                    r4 = info[30:34]
                    r4_int = int.from_bytes(r4, byteorder='big', signed=False)
                    ch4_r4 = R_chx(ch4_int,r4_int)

                    CH5 =info[10:12]
                    ch5_int = int.from_bytes(CH5, byteorder='big', signed=False)
                    r5 = info[34:38]
                    r5_int = int.from_bytes(r5, byteorder='big', signed=False)
                    ch5_r5 = R_chx(ch5_int,r5_int)

                    CH6 =info[12:14]
                    ch6_int = int.from_bytes(CH6, byteorder='big', signed=False)
                    r6 = info[38:42]
                    r6_int = int.from_bytes(r6, byteorder='big', signed=False)
                    ch6_r6 = R_chx(ch6_int,r6_int)

                    CH7 =info[14:16]
                    ch7_int = int.from_bytes(CH7, byteorder='big', signed=False)
                    r7 = info[42:46]
                    r7_int = int.from_bytes(r7, byteorder='big', signed=False)
                    ch7_r7 = R_chx(ch7_int,r7_int)

                    CH8 =info[16:18]
                    ch8_int = int.from_bytes(CH8, byteorder='big', signed=False)
                    r8 = info[46:50]
                    r8_int = int.from_bytes(r8, byteorder='big', signed=False)
                    ch8_r7 = R_chx(ch8_int,r8_int)
                    #处理客户端不正常断开
                    # except ConnectionResetError as e:
                    #     t4 = datetime.datetime.today()
                    #     sql = "insert into status(status,ip,port,connect_time) values(%s,%s,%s,%s)"
                    #     cursor.execute(sql, ["客户端不正常断开连接", client_addr[0], client_addr[1], t4])
                    #     print(f"{client_addr}不正常断开连接")
                    #     break
                    # 将数据存入数据库
                    t_recive=datetime.datetime.today()
                    sql="insert into data(ip,port,times,connect_time,CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,recive_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql,[client_addr[0],client_addr[1],(t2-t1).total_seconds(),t1,ch1_r1,ch2_r2,ch3_r3,ch4_r4,ch5_r5,ch6_r6,ch7_r7,ch8_r7,t_recive])
                    conn.commit()

                    # 回收客户端数据
                    # 服务器接收到之后，告诉客户端接到了，发送的数据类型必须是bytes，所以要编码
                    # dataSocket.send(f'服务端接收到了信息 {info}'.encode())
                except Exception as e :
                    t_error = datetime.datetime.today()# 获取现在时间
                    with open("./log.txt","w") as f:
                        f.write(f"time={t_error},e={e}")
                    print(e)
                    break
                    # dataSocket.close()
                    # cursor.close()
                    # conn.close()
                    # dataSocket, client_addr = listenSocket.accept()
                    # clientHandler(dataSocket,client_addr)
            dataSocket.close()  # 表示关闭为一个客户端的服务，accept（）会继续服务
            cursor.close()
            conn.close()
            break
# 4.等待客户端的连接
# 接受客户端的数据,处于堵塞状态
# (监听套接字负责等待新的客户端进行连接)
# （accept）产生的新的套接字用来为客户端服务
while True:
    dataSocket, client_addr = listenSocket.accept()
    print('接受一个客户端连接:', client_addr)
    # 创建新线程处理这个客户端得消息得收发
    th1=Thread(target=clientHandler,args=(dataSocket,client_addr))
    th2=Thread(target=sql_to_excel,args=(file_create_time,))
    th3 = Thread(target=create_file_time,args=(file_create_time,folder_path))
    th4 = Thread(target= data_send_email,args=(file_create_time,))
    th3.start()
    time.sleep(3)
    th1.start()
    th2.start()
    th4.start()
# 6.关闭套接字
# 服务端也调用close()关闭socket
listenSocket.close()  # 表示关闭一个服务器的服务，accept（）停止服务
## 其实我们使用Pyinstaller 打包时可以增加 -w 参数来取消cmd弹窗，即后台控制台
# pyinstaller -F -w filename.py
# 打包完成后，会生成2个文件夹，bulid 和 dist , 其中dist中存放着我们需要的 exe 程序
# 同时在当前路径下，还会生成一个同名的 .spec文件
