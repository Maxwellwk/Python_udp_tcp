import socket

# 创建用于通讯的套接字socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 设置socket对象，将socket的广播功能打开
# socket.SOL_SOCKET 表示设置的选项参数的等级 Set Option Level -SOCKET
# socket.SO_BROADCAST 表示设置广播参数，1 打开，0 关闭
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# 对于客户端可以不用绑定地址信息，操作系统会随机分配一个端口用以通讯


while True:
    # 使用sendto向对方发送数据
    # client_socket.sendto(发送的数据内容bytes类型，接收方的地址信息)
    msg = input("请输入要发送的内容: ")  # 字符串类型，通过msg.encode()编码 转换为byte类型
    # server_address = ("192.168.70.255", 8000)  # 接收方服务器的ip地址和端口号
    # 使用<broadcast>可以指明广播地址，但是不用固定死，可以达到通用
    server_address = ("<broadcast>", 8000)  # 接收方服务器的ip地址和端口号

    client_socket.sendto(msg.encode(), server_address)

    # # 接收对方发送过来的数据
    # recv_data, sender_address = client_socket.recvfrom(1024)
    # print("接收到了发送方 %s 传来的数据: %s" % (sender_address, recv_data.decode()))

# 如果不在使用套接字进行通讯，关闭套接字
# client_socket.close()
