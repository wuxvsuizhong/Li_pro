#! /usr/bin/env python

def zhuangshi(func):
    print('开始装饰...')
    def inner_func():
        print('装饰中..')
        func()
    return inner_func

@zhuangshi
def func():
    print("I want to do something in this func...")

# func()

def zhuangshi2(func):
    print('装饰2装饰中...')       #inner 之前的语句会在模块被导入的时候就执行
    def inner2():
        print('装饰2inner...')
        func()

    return inner2


print('+'*30)
@zhuangshi2
@zhuangshi       #装饰器中的inner函数之前的语句会在导入的时候按照装饰器的逆序顺序执行
def func2():
    print('I want do som ething in func2...')

# func2()