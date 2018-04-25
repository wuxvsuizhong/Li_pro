# coding:utf-8

def bubble_sort(alist):
	"""冒泡排序法"""
	n = len(alist)
	for i in range(n-1):
		for j in range(n-1-i):
			if alist[j] > alist[j+1]:
				alist[j],alist[j+1] = alist[j+1],alist[j]

def select_sort(alist):
	"""选择排序"""
	n = len(alist)
	for i in range(n-1):
		minpos = i
		for j in range(i+1,n):
			if alist[minpos] > alist[j]:
				minpos = j 	
		alist[i],alist[minpos] = alist[minpos],alist[i]


def insert_sort(alist):
	"""插入排序"""
	n = len(alist)
	for i in range(1,n):
		j = i
		while j>0:
			if alist[j] < alist[j-1]:
				alist[j],alist[j-1] = alist[j-1],alist[j]
				j -= 1
			else:
				break

def shell_sort(alist):
	"""希尔排序"""
	n = len(alist)
	gap = n//2
	while gap > 0:
		for i in range(gap,n):
			j = i
			while j > 0:
				if alist[j] < alist[j-gap]:
					alist[j],alist[j-gap] = alist[j-gap],alist[j]
					j -= gap
		gap //= 2


def quick_sort(alist,firstpos,lastpos):
	"""快速排序"""
	if firstpos >= lastpos:
		return
	mid_value = alist[firstpos]
	lowindex = firstpos
	highindex = lastpos
	while lowindex < highindex:
		while alist[highindex] >= mid_value and lowindex < highindex:
			highindex -= 1
		alist[lowindex] = alist[highindex]

		while alist[lowindex] <= mid_value and lowindex < highindex:
			lowindex += 1
		alist[highindex] = alist[lowindex]

	alist[lowindex] = mid_value

	quick_sort(alist,firstpos,lowindex)
	quick_sort(alist,lowindex+1,lastpos)


def quick_sort2(alist,firstpos,lastpos):
	"""这样的快排是不正确的，想想为什么"""
	if firstpos >= lastpos:
		return
	lowpos = firstpos
	highpos = lastpos
	mid_value = alist[lowpos] 
	while lowpos < highpos:
		while alist[highpos] >= mid_value and lowpos < highpos:
			highpos -= 1

		while alist[lowpos] <= mid_value and lowpos < highpos:	
			lowpos += 1

		if lowpos < highpos:
			temp = alist[lowpos]
			alist[lowpos] = alist[highpos]
			alist[highpos] = temp
		else:
			pass		

	quick_sort2(alist,firstpos,lowpos)
	quick_sort2(alist,lowpos+1,lastpos)


def merge_sort(alist):
	if len(alist) <= 1:#单个元素组成的不能再分割
		return alist
	mid_pos = len(alist)//2
	left_list = merge_sort(alist[:mid_pos])
	right_list = merge_sort(alist[mid_pos:])
	
	l_pos,r_pos = 0,0
	len_left = len(left_list)
	len_right = len(right_list)
	result = []
	while  l_pos < len_left and r_pos < len_right:
		if left_list[l_pos] < right_list[r_pos]:
			result.append(left_list[l_pos])
			l_pos += 1
		else:
			result.append(right_list[r_pos])
			r_pos += 1
	result.extend(left_list[l_pos:])	
	result.extend(right_list[r_pos:])
	return result








if __name__ == '__main__':
	#li = [12,11,3,4,3464,23,5,768,90]
	li = [1,3,4,2,7,6]
	#bubble_sort(li)
	#select_sort(li)
	#insert_sort(li)
	#shell_sort(li)
	#quick_sort2(li,0,len(li)-1)
	li = merge_sort(li)
	print(li)


