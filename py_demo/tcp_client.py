from socket import *

clientsock = socket(AF_INET,SOCK_STREAM)
servaddr = ("127.0.0.1",8080)
try:
	clientsock.connect(servaddr)
except ConnectionRefusedError as err:
	print('connct error '+str(err))
else:
	while True:
		senddata = input('<<')
		clientsock.send(senddata.encode('utf-8'))

		recvData = clientsock.recv(2048)
		if len(recvData) > 0:
			print('>>%s'%recvData.decode('utf-8'))
finally:
	clientsock.close()
