import socket

PORT = 8000

# 创建一个套接字socket对象，用于进行通讯
# socket.AF_INET 指明使用INET地址表集，进行网间通讯
# socket.SOCK_DGRAM 指明使用数据协议，即使用传输层的UDP协议
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 为服务器绑定一个固定的地址，ip端口号
# server_socket.bind((ip地址， 端口号))
address = ("", PORT)
server_socket.bind(address)
while True:
    # 接收客户端传来的数据 recvfrom接收客户端的数据，默认是阻塞的，等到直到有客户端传来数据
    # recvfrom 参数的意义，表示最大能接收多少数据，单位是字节
    # recvfrom 返回值说明
    # recv_date 表示接受到传来的数据，是bytes类型，recv_data.decode()解码，将bytes类型转化为字符串类型
    # client_address 表示传来的客户端的信息，客户端的ip和端口，元祖
    recv_data, client_address = server_socket.recvfrom(1024)

    print("接收到了客户端 %s 传来的数据: %s" % (client_address, recv_data.decode()))

    # 向客户端发送数据
    server_socket.sendto(recv_data, client_address)

# 不再接收数据的时候，将套接字socket关闭
# server_socket.close()

