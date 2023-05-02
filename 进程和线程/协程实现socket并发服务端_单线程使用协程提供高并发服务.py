import socket

from gevent import monkey
monkey.patch_all()  #给gevent打上monkey补丁

from gevent import spawn

def client_conn(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            conn.send(data.upper())
        except Exception:
            # windows下收到空数据会抛出异常，在这里捕获
            break
    conn.close()


def run(ip,port):
    server = socket.socket()
    server.bind((ip,port))
    server.listen()
    while True:
        conn,addr = server.accept()
        spawn(client_conn,conn)   # 使用spawn提交的任务监控client_conn的IO操作，达到有IO时切换到其他spawn监控目标任务的目的
        # 这里也就是使用spawn添加了服务端等待客户端连接accept以及服务端conn等待接收客户端消息两个IO，实现在这两个IO之间不停切换

if __name__ == '__main__':
    g = spawn(run,"127.0.0.1",6000) # spawn检测run里面的IO
    g.join()