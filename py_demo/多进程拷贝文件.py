# -*- coding:utf-8 -*-


import os
from multiprocessing import Pool,Manager
import time

def copyFileTask(fileName,queue,oldFolderName,newFolderName):
	#完成拷贝文件的功能
	fr = open(oldFolderName + '/' + fileName)
	fw = open(newFolderName + '/' + fileName,'w')

	content = fr.read()
	fw.write(content)
	time.sleep(1)
	fr.close()
	fw.close()
	
	queue.put(fileName)
	#print('put '+fileName+ ' over')


def main():
	#获取要复制的文件夹的名字
	oldFolderName = input("输入要复制的文件夹名:")

	#创建副本文件夹
	newFolderName = oldFolderName+"-copy"
	os.mkdir(newFolderName)

	#获取旧的文件夹中所有文件的名字
	filenames = os.listdir(oldFolderName)

	#线程池复制文件
	pool = Pool(5)
	queue = Manager().Queue()

	for name in filenames:
		pool.apply_async(copyFileTask,args=(name,queue,oldFolderName,newFolderName))#循环分配任务

	num = 0
	allNum = len(filenames)
	while True:
		#print('get '+str(queue.get_nowait())+' over',end='')
		queue.get()	
		num += 1
		copyRate = num/allNum
		print("当前进度:%.2f%%"%(copyRate*100),end="")#加入\r打印头归位,end=""可以使得输出不换行
		if(num == allNum):
			break#退出主进程
	
	#pool.close()
	#pool.join()

if __name__ == '__main__':
	main()
