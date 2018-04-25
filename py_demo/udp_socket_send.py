from socket import *

udpsocket = socket(AF_INET,SOCK_DGRAM)
IP = input("dest IP:")
PORT = int(input("dest port:"))
udpsocket.bind(bindAddr)
while True:
	msg = input(">>>")
	udpsocket.sendto(msg.encode("utf-8"),(IP,PORT))

