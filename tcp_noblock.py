import socket

PORT = 8080

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

address = ("", PORT)
listen_sock.bind(address)

# 将监听的socket设置为非阻塞工作方式
listen_sock.setblocking(False)

listen_sock.listen(128)

# 用来保存于服务器进行通信的所有客户端对应的socket
clients_list = []

while 1:
    # accept()返回的是一个元祖（client_socket, client_addr）
    # cilent_info = listen_sock.accept()
    # 因为已经将listen_sock设置为非阻塞，所以accept调用会立即返回，不会阻塞等待
    # 如果有客户端发起连接，accept会完成三次握手，并正确返回返回值
    # 如果没有客户端发起链接，accept不会正常返回，而是抛出异常BlockingIOError
    try:
        client_sock, client_addr = listen_sock.accept()
    except BlockingIOError as e:
        # 表示没有客户端连接
        pass
    else:
        # 表示有一个客户端的链接
        print("客户端 %s 已经链接" % (client_addr,))
        # 将客户端对应的socket设置为非阻塞
        client_sock.setblocking(False)
        # 向clients_list中保存这个链接的客户端
        clients_list.append((client_sock, client_addr))


    # 用来保存需要关闭的socket
    need_del_sock_list = []


    # 从clients_list中循环遍历处理每一个客户端
    for c_sock, c_addr in clients_list:
        # 接收客户端的数据
        # 如果客户端既没有关闭连接，也没有发送数据，recv方法会抛出异常错误BlockingIOError
        # 如果客户端关闭了链接，则recv返回空数据
        # 如果客户端没有关闭连接而是发送了数据，则recv会返回发送的数据
        try:
            recv_data = c_sock.recv(1024)
        except BlockingIOError as e:
            # 表示客户端既没有关闭连接，也没有发送数据
            pass
        else:
            if recv_data:
                # 客户端没有关闭连接而是发送了数据
                print("客户端 %s 传来了数据： %s" % (c_addr, recv_data.decode()))
            else:
                # 客户端关闭了链接
                print("客户端 %s 关闭了链接" % (c_addr,))
                c_sock.close()
                # 将需要关闭的socket添加到need_del_sock_list中，方便后面进行移除操作
                need_del_sock_list.append((c_sock, c_addr))


    # 循环遍历处理需要移除的socket
    for client_info in need_del_sock_list:
        clients_list.remove(client_info)