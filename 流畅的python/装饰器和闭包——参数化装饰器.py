# #################
# 普通的装饰器使用方式
# ##################
registry = []

def register(func):
    print(f'running register({func})')
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')

print('running main()')
print('registry ->',registry)
f1()

# 输出
# running register(<function f1 at 0x000001837A2C8F40>)
# running main()
# registry -> [<function f1 at 0x000001837A2C8F40>]
# running f1()

# #########################
# 参数化装饰器——控制装饰器的行为
# #########################
print('-'*20,"参数化装饰器控制装饰器的行为",'-'*20)
registry = set()

def register(active = True):    # register是一个装饰器工厂函数，返回装饰器
    def decorate(func):     #实际的装饰器就是这里的decorate函数
        print('running register'
              f'(active = {active}) ->decorate({func})')
        if active:      # active参数控制是否使用装饰器，True时启用
            registry.add(func)
        else:
            registry.discard(func)  # active参数为False时，从registry中移除被装饰的func函数
        return func
    return decorate     #这里直接返回的才是装饰器函数，用这里返回的函数去装饰

@register(active=False)
def f1():
    print('running f1()')

# @register #error 这里需要使用register()调用来返回装饰器
@register()     # 不传递参数这里的register默认的active参数为True
def f2():
    print('running f2()')

def f3():
    print('running f3()')

# ###################
# 一个参数化装饰器的例子
# ###################
print('-'*20,"参数化装饰器控制装饰器的行为——参数化clock装饰器",'-'*20)

import time

# 自定义打印的格式
DEFAULT_FMT = '[{elaspsed:0.8f}s] {name} {args}) -> {result}'


def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*args):
            t0 = time.perf_counter()
            _result = func(*args)
            elaspsed = time.perf_counter() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in args)
            result = repr(_result)
            print(fmt.format(**locals()))  # 使用自定义的格式fmt格式化, **locals()是为了先获取clocked这个函数的局部边浪，然后对其进行拆包后作为参数传入fmt.format中，DEFAULT_FMT这个格式化的字符串中的几个变量elaspsed，name，args，result分别对应**locals()拆包后的变量
            # print(locals())
            return _result
        return clocked  # decorate返回clocked
    return decorate # clock返回decorate，decorate才是真正的装饰器

if __name__ == "__main__":
    @clock()    # clock函数是装饰器的工厂方法，需要使用()对clock进行调用来返回真正的装饰器decorate
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)

    # 给工厂方法传递参数，自定义格式
    @clock('{name}: {elaspsed}s')
    def snooze2(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze2(.123)

    # 给工厂方法传递参数，自定义格式
    @clock('{name}({args}) dt={elaspsed:0.3f}s')
    def snooze3(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze3(.123)

# ###############################
# 基于类的装饰器——定义类的__call__方法
# ###############################
# 装饰器是一个类

# 自定义打印的格式
DEFAULT_FMT = '[{elaspsed:0.8f}s] {name} {args}) -> {result}'
class clock:
    '''类装饰器'''
    def __init__(self,fmt=DEFAULT_FMT):
        self.fmt = fmt

    def __call__(self, func):   # func是被装饰函数
        def clocked(*_args):    # 被装饰的函数func的形参传递在_args中
            t0 = time.perf_counter()
            _result = func(*_args)
            elaspsed = time.perf_counter() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(self.fmt.format(**locals()))
            return result
        return clocked
