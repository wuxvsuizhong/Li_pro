#coding:utf-8



def binary_search(alist,item):
	"""二分查找,递归实现"""
	n = len(alist)
	if n > 0: 
		mid_pos = n//2
		if  alist[mid_pos] == item:
			return True
		elif item < alist[mid_pos]:
			return binary_search(alist[:mid_pos],item)
		else:
			return binary_search(alist[mid_pos+1:],item)

	return False

def binary_search2(alist,item):
	n = len(alist)
	first_pos = 0
	last_pos = n-1
	while first_pos <= last_pos:#当定位到最后没有找到的时候，first_pos > last_pos出现,返回False
		mid = (first_pos + last_pos)//2
		
		if item == alist[mid]:
			return True
		elif item < alist[mid]:
			last_pos = mid-1
		else:
			first_pos = mid+1
	return False




if __name__ == '__main__':
	li = [2,3,4,5,6]
	print(binary_search2(li,1))
