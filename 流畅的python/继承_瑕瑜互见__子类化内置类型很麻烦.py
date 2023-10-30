# ##################################
# 内置类型通常不调用用户自定义的类覆盖方法
# ##################################
print('-'*20,"内置类型通常不调用用户自定义的类覆盖方法",'-'*20)

class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key,[value]*2)

dd = DoppelDict(one = 1)
print(f'{dd!r}')    # {'one': 1} 本意是要调用DoppelDict的__setitem__，会把存入的值重复两次，但是这里并没有调用
# 继承自dict的__setitem__方法被忽略
dd['two'] = 2
print(f'{dd!r}')    # {'one': 1, 'two': [2, 2]}  使用[]赋值可以正常调用重写的__setitem__
dd.update(three = 3)
print(f'{dd!r}')    # {'one': 1, 'two': [2, 2], 'three': 3}     #使用update无法调用重写的__setitem__

class AnswerDict(dict):
    def __getitem__(self, key):
        return 42

ad = AnswerDict(a='foo')
print(ad['a'])      # 42 无论传入什么，始终返回42
d = {}
d.update(ad)
print(d['a'])   # foo   并没有返回42，update忽略了重写的__getitem__方法
print(d)        # {'a': 'foo'}

# 直接子类化内置类型(list,dict,str等)容易出错,应为内置的类型通常忽略用户覆盖的方法，
# 不要子类化了内置类型，用户自定义的类应该继承collections模块中的类，如UserdDict,UserList,UserString

##########################
# 继承自collcection模块中的类
##########################
print('-'*20,"继承自collcection模块中的类",'-'*20)
import collections
class DoppleDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key,[value]*2)

dd = DoppleDict2(one=1)
print(dd)   # {'one': [1, 1]}
dd['teo'] = 2
print(dd)   # {'one': [1, 1], 'teo': [2, 2]}
dd.update(three = 3)
print(dd)   # {'one': [1, 1], 'teo': [2, 2], 'three': [3, 3]}

class AnswerDict2(collections.UserDict):
    def __getitem__(self, key):
        return 42

ad = AnswerDict2(a='foo')
print(ad['a'])  # 42
d={}
d.update(ad)
print(d['a'])   # 42
print(d)        # {'a': 42}

# 内置类型在Cpython中由C语言实现的，如果直接继承会使得重写的一些方法__setitem__,__getitem__被忽略
# 因此如果要子类化内置类型，需要子类化使用python编写的类UserDict,MutableMapping等
