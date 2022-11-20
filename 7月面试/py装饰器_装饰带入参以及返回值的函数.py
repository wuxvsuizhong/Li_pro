#! /usr/bin/env python

def zhuangshi(func):
    print('开始装饰...')
    def inner(a,b):
        print('装饰中...')
        func(a,b)
        print('装饰结束')

    return inner

@zhuangshi
def test(a,b):
    print('计算{}+{}={}'.format(a,b,a+b))

test(1,2)

print('+'*30)

def zhuangshi2(func):
    print('开始装饰...')
    def inner(a,b):
        print('装饰中...')
        ret = func(a,b)
        print('装饰完毕')
        return ret     #被装饰的func如果带有return 只,那么inner也必须带return 值

    return inner

@zhuangshi2
def test2(a,b):
    return a+b

result = test2(1,2)
print(result)

#不定个数入参装饰
def zhuangshi3(func):
    print('装饰开始...')
    def inner(*args,**kwargs):
        print('装饰中...')
        ret = func(*args,**kwargs)
        print('装饰结束')
        return ret

    return inner

@zhuangshi3
def test3(*args,**kwargs):
    sum=0
    for each in args:
        sum += each

    return sum

result3 = test3(1,2,3,4,5)
print(result3)
