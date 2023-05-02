import socket

client = socket.socket()
client.connect(("127.0.0.1",6000))

while True:
    # input()
    client.send(b'hello')
    data = client.recv(1024)
    print(data)