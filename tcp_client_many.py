import socket


# 创建socket对象，用于通信
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 对于客户端，可以不用绑定一个固定的地址，使用操作分配的即可

# 向服务器发起请求连接，并完成三次握手
server_addr = ("127.0.0.1", 9000)
client_sock.connect(server_addr)

while 1:
    # 向服务器发送数据
    msg = input("请输入要发送的数据")
    if msg == "quit":
        # 如果输入quit则退出，关闭连接
        # 如果客户端不想再次发送数据，可以关闭链接
        client_sock.close()
        break
    else:
        client_sock.send(msg.encode())

        # 接收服务器传回的数据
        recv_data = client_sock.recv(1024)
        print("收到了由服务器传回的数据: %s " % recv_data.decode())



