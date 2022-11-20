#! /usr/bin/env python
import types


class Person(object):
    def __init__(self,name):
        self.name=name


p=Person('abc')
print(p.name)

def running(self):
    print('{}正在跑'.format(self.name))

ret = types.MethodType(running,p)
ret()

