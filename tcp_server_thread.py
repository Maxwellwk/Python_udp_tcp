import socket

from threading import Thread

# 服务器的端口号
PORT = 9000

# 创建套接字socket对象，用于进行通讯
# socket.SOCK_STREAM 表明使用tcp协议，流式协议
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 为socket对象设置重用地址参数，以便程序重新启动的时候，还能够使用同一个端口
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 为服务器的socket绑定一个固定的地址，ip和端口，元祖
address = ("", PORT)
server_sock.bind(address)

# 让服务器开启监听，可以收到客户端的链接请求
# listen参数表示监听队列的大小，最多能同时处理三次握手的客户端的数量
server_sock.listen(128)
print("服务器已经开启了监听")


def handle_client(client_sock, client_addr):
    """子进程处理客户端的行为"""
    # 表示与这个客户端可以进行多次数据传输（发送接收）
    while 1:
        # 接收客户端的数据
        # recv方法的返回值，如果返回空字节类型数据，表示已经关闭了链接
        # 如果返回的不是空数据，表示对方没有关闭连接，而是发送过来了数据
        recv_data = client_sock.recv(1024)

        if recv_data:
            # 表示recv_data不是空数据，即客户端没有关闭连接
            print("接收到了客户端 %s 传来的数据: %s" % (client_addr, recv_data.decode()))

            # 向客户端发送数据
            client_sock.send(recv_data)
        else:
            # 表示recv_data是空数据，及客户端已经关闭了链接
            print("客户端 %s 已经关闭了连接" % (client_addr,))
            # 如果没有数据再传给客户端，可以关闭连接
            client_sock.close()
            break


# 表示可以循环多次接收客户端的链接请求，与客户端完成三次握手
while 1:
    # 接收客户端的链接请求，与客户端完成三次握手
    # accept函数是阻塞的，如果当前没有客户端发起链接，则会阻塞等待直到有客户端发起连接
    # new_sock是一个新的socket对象，用来跟这个链接的客户端进行一对一的数据传输使用
    # client_addr是建立连接的客户端地址，ip和端口， 元祖
    new_sock, client_addr = server_sock.accept()

    # print("客户端 %s 已经建立了链接" % str(client_addr))
    print("客户端 %s 已经建立了链接" % (client_addr,))

    # 创建子线程，负责处理这个链接的客户端
    t = Thread(target=handle_client, args=(new_sock, client_addr))
    t.start()


# # 如果没有数据要传输可以关闭连接
# new_sock.close()
#
# # 如果不想再接收新的客户端请求，可以关闭server_sock
# server_sock.close()