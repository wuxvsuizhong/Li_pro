#! /usr/bin/env python

def zhuangshi(arg):
    print('BEGIN...')
    def inner1(func):         #inner1 作为一个新的装饰器装饰入参func
        print('innner1...')
        def realinner():            #test()就是小勇这一层的realinner
            print('realinner...')
            func()
        return realinner
    return inner1


@zhuangshi('abc')   #带入参的装饰器不会立即装饰test,他自身会先调用一层函数返回一个新的函数，用这个新的函数去装饰test
def test():
    print('test........')
test()