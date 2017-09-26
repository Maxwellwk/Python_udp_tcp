import socket

# 创建用于通讯的套接字socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 对于客户端可以不用绑定地址信息，操作系统会随机分配一个端口用以通讯使用
# 使用sendto向对方发送数据
# client_socket.sendto(发送数据内容byte类型，接收方的地址信息)
while True:
    msg = input("请输入要发送的内容: ")  # 字符串类型，通过msg.encode()编码 转换为byte类型
    server_address = ("127.0.0.1", 8080)  # 接收方服务器的ip地址和端口号
    client_socket.sendto(msg.encode(), server_address)

    # 接收对方发送过来的数据
    recv_data, sender_address = client_socket.recvfrom(1024)
    print("接收到了发送方 %s 传来的数据: %s" % (sender_address, recv_data.decode()))

# 如果不在使用套接字进行通讯，关闭套接字
# client_socket.close()
