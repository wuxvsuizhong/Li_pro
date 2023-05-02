import socket
import select

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(("127.0.0.1",7000))
server.listen(5)
server.setblocking(False)  #设置socket非阻塞模式

readList = []
readList.append(server)

# 使用select统一监管可读对象列表，包含服务端的监听套接字server以及客户端建立的连接conn
while True:
    rlist,wlist,xlist  = select.select(readList,[],[])  #只监控可读对象列表readList
    for each in rlist:
        print(each)
        if each is server:  # 可读的对象是服务端的监听socket——server
            conn,addr = server.accept()
            readList.append(conn) # 如果可读的是客户端的连接conn，那么也同样把conn连接对象追加到readList中
            continue
        else: # 可读的是客户端的连接conn
            try:
                data = each.recv(1024)
                if not data: # 在linux上，接收到的数据为空，表示客户端已经断开连接
                    each.close()
                    readList.remove(each)  # 从监管列表中删除监听对象conn
                    continue
                else: # conn接收到了消息，会给客户端一个消息
                    each.send(data.upper())
            except ConnectionResetError:  # windows下断开conn连接，服务端会抛出异常，处理这个异常
                each.close()
                readList.remove(each)
                continue


# select 在windows和linux都是支持的，但是监管数量由限制，在32位机器上最大支持1024，在64位机器上最大支持2048
# select监管的缺点是，在大量并发的时候，部分的连接可能不能得到及时的响应，比如在select轮询可读对象列表的过程中
# 如果前一个可读的对象在之前那还不可读，但是如果轮训到下一个对象的时候，前一个对象突然可堵了，那么也得等到下一次轮训到它的时候才会读取它里面的数据