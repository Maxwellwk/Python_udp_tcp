import socket
import select

PORT = 8080

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

address = ("", PORT)
listen_sock.bind(address)

listen_sock.listen(128)

# 创建epoll容器
epoll = select.epoll()
# 向epoll中注册需要epoll监视的socket资源，以文件编号的方式交给epoll
# select.EPOLLIN表示让epoll帮助我们监视什么时候数据发送过来
# select.EPOLLOUT表示监管什么时候能够向外发送数据
epoll.register(listen_sock.fileno(), select.EPOLLIN)

# 保存产生的客户端的socket对象与编号
sock_dick = {}

while 1:
    # 询问epoll有哪些socket能够进行工作，返回的是socket对象文件的编号
    socket_fd_list = epoll.poll()  # socket_fd_list == [(socket文件的编号，发生的行为epollin还是epollout事件),(),()]

    # 遍历socket_fd_list的，对每一个socket进行处理
    for sock_fd, event in socket_fd_list:
        # 判断这个socket是不是监听的socket
        if sock_fd ==listen_sock.fileno():
            # 是监听的socket
            client_sock, client_addr = listen_sock.accept()
            print("客户端 %s 已连接" % (client_addr,))
            # 将socket保存到sock_dict中
            sock_dick[client_sock.fileno()] = client_sock
            # 将新建立链接的socket添加到epoll中
            epoll.register(client_sock.fileno(), select.EPOLLIN)
        else:
            # 不是监听的socket，而是新添加的与客户端通信的socket
            sock = sock_dick[sock_fd]
            recv_data = sock.recv(1024)
            if recv_data:
                print("客户端传来的数据： %s" % recv_data.decode())
            else:
                print("客户端已经关闭了链接")
                sock.close()
                # 从epoll中移除这个已经关闭了链接的socket
                epoll.unregister(sock_fd)
                del sock_dick[sock_fd]



