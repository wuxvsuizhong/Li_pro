import socket
from threading import Thread,current_thread

client = socket.socket()
client.connect(("127.0.0.1",6000))

def t_client():
    n = 0
    while True:
        msg = f"{current_thread().name} say {n}"
        client.send(msg.encode('utf-8'))  # 在循环内不间断的向服务端发送消息
        data = client.recv(1024)  #接收的是从服务端返回的小写转大写的字符串
        print(data.decode('utf-8'))
        n += 1


if __name__ == '__main__':
    for i in range(1000):  #模拟1000个客户端去连接服务器
        t = Thread(target=t_client)
        t.start()
