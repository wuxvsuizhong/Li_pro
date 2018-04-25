from socket import *
from treading import Thread
import struct

#客户端上传文件线程函数
def upload_thread(file_name,client_info):
	filenum = 0
	f = open(file_name,'wb')
	s = socket(AF_INET,SOCK_DGRAM)

	#首次回应客户端的请求
	res_data_start = struct.pack("!HH",4,filenum)
	s.sendto(res_data_start,client_info)

	while True:
		#接受客户端发来的数据
		recv_data_from_client = s.recvfrom(1024)
		recv_data,client_info = recv_data_from_client

		#解包
		pack_opt = struct.unpack("!H",recv_data[:2])#解包操作码
		pack_num = struct.unpack("!H",recv_data[2:4])#解包包序号

		if pack_opt == 3 and pack_num == filenum:
			f.write(recv_data[4:])
			#回应客户端数据
			res_data_to_client = struct.pack("!HH",4,filenum)
			
			s.sendto(res_data_to_client,client_info)
			filenum += 1

			if len(recv_data) < 516:
				print("用户"+str(client_info),end="")
				print("上传"+file_name+"完成！")
				break

	f.close()
	s.close()
	exit()


#客户端下载文件线程
def download_thread(file_name,client_info):
	s = socket(AF_INET,SOCK_DGRAM)

	filenum = 0

	try:
		f = open(file_name,'rb')

	except:
		err_res = struct.pack("!HHHb",5,5,5,filenum)
		s.sendto(err_res,client_info)
		exit()
	
	
	read_file_data = f.read(512)

	#首次回应客户端请求,块编号为0,发送一个数据包
	res_data_pack = struct.pack("!HH",3,filenum)+read_file_data
	sendbytes = s.sendto(res_data_pack,client_info)	
	
	while True:
		if sendbytes == res_data_pack:
			if sendbytes < 516:
				print("向客户端"+str(client_info+"传输文件完成!"))
				break
		else:
			print("向客户端"+str(client_info+"传输文件出错!"))
			break

		#接收客户端ack回应
		recv_data = s.recvfrom(1024)
		recv_data_info,client_info = recv_data
		recv_pack_opt = struct.unpack("!H",recv_data_info[:2])
		recv_pack_num = struct.unpack("!H",recv_data_info[2:4])

		
		if recv_data_opt == 4 and recv_pack_num == filenum:
			filenum += 1
			res_data_pack = struct.pack("!HH",3,filenum)+f.read(512)
			sendbytes = s.sendto(send_data,client_info)
		else:
			print("向客户端"+str(client_info+"传输文件出错!"))
			break

	f.close()
	s.close()
	exit()

		
if __name__ == '__main__':
	#生成一个套接子专门用于接收客户端的链接请求	
		
