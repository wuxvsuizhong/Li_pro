import socket

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  #设置可以重用绑定设置
server.bind(("127.0.0.1",7000))
server.listen(5)
server.setblocking(False) # 设置所有的网络阻塞变为非阻塞

c_list = []  # 已建立的连接的conn列表
conn_del_list = [] # 已经断开连接的conn的列表（即将被清理的conn的列表)）


while True:
    try:
        conn,addr = server.accept()  # 非阻塞模式下，无连接会直接抛出BlockingIOError
        c_list.append(conn) # 非阻塞模式下，有连接才会执行到这里，把连接添加到列表里
    except BlockingIOError:  # 非阻塞模式下，无连接的时候轮询历史已经建立连接的conn列表
        # print("无连接，做些别的事情...")
        print("连接的客户端数量",len(c_list))
        for conn in c_list:
            try:
                data = conn.recv(1024)   # 非阻塞的socket,如果没有接收到数据会抛出异常BlockingIOError
                if not data: #linux下接收数据就空代表断开连接
                    conn.close()
                    conn_del_list.append(conn)  #把要断开的连接conn对象移动到其他的列表中
                else:
                    # 接收到了数据，再返回给客户端
                    conn.send(data.upper())  # 已连接的conn接收到数据后发送数据给客户端
            except BlockingIOError: #非阻塞模式下,conn没有接收到数据那么跳过，循环继续监测下一个conn
                pass
            except ConnectionResetError: #windos断开连接会在服务端连接抛出 ConnectionResetError异常，所以在这里也处理一下
                conn.close()
                conn_del_list.append(conn)

        for d in conn_del_list: # 清理需要关闭的客户端连接
            c_list.remove(d)  # 把关闭的conn对象从conn列表中删除
        conn_del_list.clear() # 清理已关闭的conn对象列表

# 总结:非阻塞模式下，socket会不停的在监听accept和检测已连接的conn列表轮询这两者之间不断切换
# 如果有连接那么计入到conn的列表c_list中
# 如果轮询conn列表检测到连接断开那么把conn先加入到需要移除的列表conn_del_list中，一轮轮询完成后，遍历conn_del_list清理已经断开的连接
# 轮询已经连接的conn列表如果发现有连接发送了数据过来那么当即返回给客户端响应
# 这个模型的缺点就是一直轮询，会消耗CPU资源