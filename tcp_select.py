import socket
import select

PORT = 8080

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

address = ("", PORT)
listen_sock.bind(address)

listen_sock.listen(128)

# 构建让socket选择有哪些socket有数据传来的列表
input_sock_list = [listen_sock]

while 1:
    # 调用select函数，帮助我们从socket列表中选择出有需求的socket
    recv_accept_sock_list, send_sock_list, Exception_sock_list = select.select(input_sock_list, [], [])

    # 遍历返回值，对socket进行处理
    for sock in recv_accept_sock_list:
        if sock == listen_sock:
            # 如果返回值中返回的是监听的socket
            client_sock, client_addr = sock.accept()
            print("客户端 %s 已连接" % (client_addr,))
            # 将于客户端通讯的socket添加到Input_sock_list中，让select下次选择的时候，
            # 能够帮助我们判断，这个客户端有没有数据发送过来
            input_sock_list.append(client_sock)
        else:
            # 如果不是监听的socket，表示是新添加的客户端的socket，可以接受数据
            recv_data = sock.recv(1024)
            if recv_data:
                # 客户端传来了数据
                print("客户端传来了数据: %s " % recv_data.decode())
            else:
                # 客户端关闭了链接
                print("客户端关闭了链接")
                sock.close()
                # 从input_sock_list中移除这个关闭了链接的客户端socket，不需要select再帮助我们选择过滤了
                input_sock_list.remove(sock)