import selectors
import socket

# selectors 会自动根据运行的瓶体win,linux,mac等选择内部的监管机制是select还是epoll

server = socket.socket()
server.bind(("127.0.0.1",6000))
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,10)
server.setblocking(False)
server.listen(5)

def accept(server : socket.socket):
    conn,addr = server.accept()
    sel.register(conn,selectors.EVENT_READ,read)

def read(conn):
    try:
        data = conn.recv(1024)
        if not data:
            conn.close()
            sel.unregister(conn)
            return
        else:
            conn.send(data.upper())
    # except BlockingIOError:
    #     pass
    except ConnectionResetError:
        conn.close()
        sel.unregister(conn)
        return


sel = selectors.DefaultSelector()  #创建selectors监管对象
sel.register(server,selectors.EVENT_READ,accept)   #第一个参数是要监管的对象，第二个参数是在可读还是可写的时候触发，第三个参数是回调函数，也就是在server可读的时候，触发将对象放入就绪列表

# 轮询可读列表
while True:
    # selector 监管的时候，当对象可读的时候会自动把对象加入到可读列表，但是不会自动调用对象的回调函数
    # 所以需要我们遍历就绪列表，逐个调用就序列表中可读对象的回调函数
    events = sel.select()  # 调用监管对象的select方法，获取就绪列表
    for key,event_type in events:  #就绪列表中的每一个元素都是元组类型，元组中有两个变囊
        # 第一个就是就绪的对象和附带的一些成员(包括可读对象本身fileobj，以及系统的文件描述符fd，注册的回调函数data等)，
        # 第二个就是就绪对象被触发为就绪时，触发它的事件类型，这里也就是 selectors.EVENT_READ
        callback = key.data   # key.data 取出对象注册的回调函数
        callback(key.fileobj) # key.fileobj就是可读对象本身
        # 因为在对象注册到seletors里的时候，添加了回调函数，所以这里在就绪列表中获取可读对象时，可以获取到对象当时注册的回调函数
        # server注册的是accept,conn注册的是read,这里当它们可读就绪时，就自动识别了当时注册的回调函数，从而发起调用
