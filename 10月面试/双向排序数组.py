'''
输入整型数组和排序标识，对其元素按照升序或降序进行排序

数据范围：1≤n≤1000  ，元素大小满足0≤val≤100000
输入描述：
第一行输入数组元素个数
第二行输入待排序的数组，每个数用空格隔开
第三行输入一个整数0或1。0代表升序排序，1代表降序排序

输入：
8
1 2 4 9 3 55 64 25
0
输出：
1 2 3 4 9 25 55 64
复制

示例2
输入：
5
1 2 3 4 5
1
输出：
5 4 3 2 1
'''
import sys

def main():
    quantity = int(sys.stdin.readline().strip())
    nums = list(map(int,input().strip().split()))
    direction = int(input().strip())

    for i in range(1,len(nums)):
        for j in range(len(nums)-i):
            if direction == 0 and nums[j] > nums[j+1]:
                nums[j],nums[j+1] = nums[j+1],nums[j]
            elif direction == 1 and nums[j] < nums[j+1]:
                nums[j],nums[j+1] = nums[j+1],nums[j]
            else:
                pass

    print(nums)



if __name__ == '__main__':
    main()