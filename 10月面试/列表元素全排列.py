def all_combs(result,num_list):
    """数据的全排列"""
    if not num_list:
        print(result)
        return
    for i in range(len(num_list)):
        all_combs(result+str(num_list[i]),num_list[:i]+num_list[i+1:])
print('-'*20,'数据全排列','-'*20)
all_combs('',[1,2,3])

def all_ncombs(result,num_list,n):
    """数组中n个数据的全排列"""
    if n <= 0:
        print(result)
        return
    for i in range(len(num_list)):
        all_ncombs(result+str(num_list[i]),num_list[:i]+num_list[i+1:],n-1)
        # all_ncombs(result+str(num_list[i]),num_list[i+1:],n-1)  # 如果不再选择i的前向的元素，那么就是不走回头路，得到的是组合，而非全排列


print('-'*20,'抽取n个数据全排列','-'*20)
all_ncombs('',[1,2,3,4],2)

def any_combs(num_list):
    result=[]
    lst=[]

    def get_combs(num_list: list,result: list,lstL:list,pos: int):
        if lst: result.append(lst[:])
        for i in range(pos,len(num_list)):
            lst.append(num_list[i])
            get_combs(num_list,result, lst, i+1)
            lst.pop()

    get_combs(num_list,result,lst,0)
    print(result)
    return

print('-'*20,'获取任意个数的全排列','-'*20)
any_combs([1,2,3])




