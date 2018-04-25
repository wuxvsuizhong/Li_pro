from socket import *

servsock = socket(AF_INET,SOCK_STREAM)
bindAddr = ("",8080)
servsock.bind(bindAddr)
servsock.setblocking(False)

servsock.listen(100)

client_sockets=[]


while True:
	#先循环接受链接请求，然后循环接受数据
	try:
		clientsock,clientinfo = servsock.accept()
	except:
		pass
	else:
		print('new connet%s'%str(clientinfo))
		clientsock.setblocking(False)#分配给客户端的套接字也设置为非阻塞
		client_sockets.append((clientsock,clientinfo))
	
	for eachsock,eachsock_info in client_sockets:
		try:
			recvdata = eachsock.recv(1024)
		except:
			pass
		else:
			if len(recvdata) == 0:
				print('(%s) disconnect!'%str(eachsock_info))
				eachsock.close()
				client_sockets.remove((eachsock,eachsock_info))
			else:
				print(">>(%s) %s"%(str(eachsock_info),recvdata))
