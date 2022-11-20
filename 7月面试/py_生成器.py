#! /usr/bin/python

def fib(num):
    a,b = 0,1
    for i in range(num):
        a,b = a+b,a
        yield a


f=fib(9)
for i in f:
    print(i)


def func(num):
    i=0
    while i < num:
        i+=1
        temp = yield i
        print(temp)

f1 = func(5)
print(f1.send(None))
print('--------------')
print(f1.send('haha'))
print(next(f1))
