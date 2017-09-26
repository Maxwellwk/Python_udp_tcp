import socket

# 服务器的端口号
PORT = 8080

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

# 接收客户端的链接请求，与客户端完成三次握手
# accept函数是阻塞的，如果当前没有客户端发起链接，则会阻塞等待直到有客户端发起连接
# new_sock是一个新的socket对象，用来跟这个链接的客户端进行一对一的数据传输使用
# client_addr是建立连接的客户端地址，ip和端口， 元祖
new_sock, client_addr = server_sock.accept()


# print("客户端 %s 已经建立了链接" % str(client_addr))
print("客户端 %s 已经建立了链接" % (client_addr,))

# 接收客户端的数据
recv_data = new_sock.recv(1024)

print("接收到了客户端 %s 传来的数据: %s" % (client_addr, recv_data.decode()))


# 向客户端发送数据
msg = input("请输入要传给客户端的数据: ")
new_sock.send(msg.encode())

# 如果没有数据要传输可以关闭连接
new_sock.close()

# 如果不想再接收新的客户端请求，可以关闭server_sock
server_sock.close()