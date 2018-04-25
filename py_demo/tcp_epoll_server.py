from socket import *
import select

s = socket(AF_INET,SOCK_STREAM)
bind_addr = ("",8080)
s.bind(bind_addr)
s.listen(100)
epoll = select.epoll()

epoll.register(s.fileno(),select.EPOLLIN|select.EPOLLET)
#注册套接字文件描述符
#EPOLLIN表示检测能读的文件描述符对应的设备
#EPOLLOUT表示检测能写的文件描述符对应的设备
#EPOLLET表示按照边沿沿检测(也就是只检测第一次可读)

connections = {}
address = {}

while True:
	epoll_list = epoll.poll()#epoll进行扫描 --没指定超时时间那么超时等待

	for fd,events in epoll_list:
		if fd == s.fileno():
			conn,addr = s.accept()
			print('new connection%s'%str(addr))
			connections[conn.fileno()] = conn
			address[conn.fileno()] = addr
			print(str(connections)+ str(address))
			epoll.register(conn.fileno(),select.EPOLLIN)

		elif events == select.EPOLLIN:#有可以读的
			recvData = connections[fd].recv(1024)
			if len(recvData) > 0:
				print("recv:%s"%str(recvData))
			else:
				epoll.unregister(fd)
				connections[fd].close()
				print("%s offline"%str(address[fd]))


