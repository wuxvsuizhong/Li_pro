#####################
# 局部变量和全局变量
#####################

b=6
def f2(a):
    print(a)
    # print(b)    # UnboundLocalError: cannot access local variable 'b' where it is not associated with a value
    b=9     # 因为变量b在函数内部被赋值，所以python判断其为一个local变量，但是在上一个语句print(b)时，b还没有被赋值，所以会在打印的时候报错
f2(3)
print('-'*20)
# 要想在赋值给全局变量的时候，不报错，粗腰添加global声明
b=6
def f3(a):
    global b
    print(a)    # 3
    print(b)    # 6
    b = 9

f3(3)
print(b) # 9 全局变量b在函数f3中被重新赋值为9

##############
# 闭包
##############

print('-'*20+'存储数据在类属性中'+'-'*20)
class Average():
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)

avg = Average()
print(avg(10))
print(avg(11))
print(avg(12))

print('-'*20+'存储数据在自由变量中'+'-'*20)
def make_average():
    series = []     # 自由变量——未在局部 作用域中绑定的变量
    # 因为series是一个列表，是可变类型，所以追加操作在average内部不会导致重新绑定，其可以一直留在自由变量中

    def average(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)

    return average

avg = make_average()
print(avg(10))
print(avg(11))
print(avg(12))
print(avg.__code__.co_varnames)     # 获取局部变量 ('new_value', 'total')
print(avg.__code__.co_freevars)     # 获取自由变量 ('series',)
print(avg.__closure__)              # 获取自由变量的元素项
print(avg.__closure__[0].cell_contents)     #获取自由变量的元素项的值

##########################
# 不可便类型在局部赋值或修改
##########################
def make_average():
    total = 0
    count = 0

    def average(new_vcalue):
        count += 1
        total += new_vcalue     # 和count一样，total也是一个数值类型，数值，字符串，元组等不可变类型只能读取，不能更新
        # 不可变类型在原地追加，这样会尝试重新绑定，会隐式的重新创建局部变量 count和total,如此一类，其就不是自由变量，不会被保存在闭包中
        return total/count
    return average
avg=make_average()
# print(avg(10))            #UnboundLocalError: cannot access local variable 'count' where it is not associated with a value


##########################
# 引入nonlocal 关键字
##########################
print('-'*20+'nonlocal 访问次外一层的局部变量'+'-'*20)
def make_average():
    count = 0
    total = 0

    def average(new_value):
        nonlocal count,total
        count += 1
        total += new_value
        return total/count
    return average

avg = make_average()
print(avg(10))
print(avg(11))
print(avg(12))

# nonlocal和global的区别在于。nonlocal只能限定访问次外一层的局部变量，而global是变量作为全局可访问的变量去查找
# nonlocal能达到的范围限定更小，也更安全
# 如果变量申明在了闭包函数中的不可变的局部变量(也就是自由变量)，那么是无法再内层函数中使用global的，此时只能使用nonlocal