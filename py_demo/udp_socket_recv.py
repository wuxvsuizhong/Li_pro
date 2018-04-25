from socket import *

udpsocket = socket(AF_INET,SOCK_DGRAM)
bindAddr = ("",8080)
udpsocket.bind(bindAddr)
while True:
	recvdata = udpsocket.recvfrom(1024)
	print(recvdata[0].decode('utf-8'))


udpsocket.close()

