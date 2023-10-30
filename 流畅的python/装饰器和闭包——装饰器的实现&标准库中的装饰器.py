import time

def clock(func):
    def clocked(*args):     # 内部函数clocked，接受位置参数
        开始 = time.perf_counter()
        result = func(*args)    # clocked函数中包含自由变量func
        过程时长 = time.perf_counter() - 开始
        name = func.__name__
        arg_str = ' ,'.join(repr(arg) for arg in args)
        print(f'[{过程时长:0.8f}s] {name}({arg_str}) -> {result}')
        return result
    print('clocked中的自由变量：',clocked.__code__.co_freevars)    #clocked中的自由变量： ('func',)
    return clocked

@clock
def snooze(seconds):
    '''睡眠函数'''
    time.sleep(seconds)

@clock
def factorial(n):
    '''计算阶乘'''
    return 1 if n < 2 else n*factorial(n-1)     # 计算阶乘


if __name__ == "__main__":
    print('*'*40,'calling snooze(.123)')
    snooze(.123)
    print('*'*40,'calling factorial(6)')
    factorial(6)

    print(factorial.__name__,factorial.__doc__)   # clocked

# 输出为
# clocked中的自由变量： ('func',)
# clocked中的自由变量： ('func',)
# **************************************** calling snooze(.123)
# [0.12424300s] snooze(0.123) -> None
# **************************************** calling factorial(6)
# [0.00000140s] factorial(1) -> 1
# [0.00002790s] factorial(2) -> 2
# [0.00004880s] factorial(3) -> 6
# [0.00006890s] factorial(4) -> 24
# [0.00008760s] factorial(5) -> 120
# [0.00010950s] factorial(6) -> 720
# clocked None


# 总结：装饰器时闭包的一种使用形式，
# 在闭包中，自由变量一种是在闭包函数中的局部变量，一种则是在闭包函数接收到的形参，如上面的clock函数接受的func
# 使用装饰器时，被装饰函数是在闭包函数的最外层形参func中传递，被装饰函数的传参则是在闭包函数的内层def的函数新参上进行传递
# 装饰器返回的一般都是闭包函数内层def的函数的引用，在闭包函数内部的def函数中会返回函数的运行结果(在被装饰函数真正调用时才会运行返回)
# 经过装饰器装饰的函数后，函数原来的__name__和__doc__属性将会被遮盖

############################################################################
# 使用@functools.wraps 装饰器还原对被装饰函数的__name__和__doc__属性的访问
############################################################################
import functools
def newclock(func):
    @functools.wraps(func)          # 使用functools.wrap装饰器装饰func,保留对被装饰函数func的__name__和__doc__的访问
    def clocked(*args,**kwargs):    # 增加了接受关键字参数
        开始 = time.perf_counter()
        result = func(*args,**kwargs)
        经历时长 = time.perf_counter() - 开始
        name = func.__name__
        arg_lst = [repr(arg) for arg in args]
        arg_lst.extend(f'{k} = {v!r}' for k,v in kwargs.items())
        arg_str = ', '.join(arg_lst)
        print(f'[{经历时长:.8f}s] {name}({arg_str}) -> {result!r}')
        return result
    return clocked

@newclock
def f3(n):
    """测试functools.wrap装饰后的函数"""
    time.sleep(n)
    print('f3() running finish...')

# 使用functools.warp装饰器修饰被装饰函数func后，被装饰函数的原属性会保留访问
print(f3.__name__,f3.__doc__)   #f3 测试functools.wrap装饰后的函数

############################################################################
# 使用@functools.cache 装饰器做备忘
############################################################################
print("-"*20,'使用functools.cache做函数备忘——未使用caceh前','-'*20)
@newclock
def fib(n):
    return n if n<2 else fib(n-2)+fib(n-1)

print(fib(6))
# 输出
# [0.00000110s] fib(0) -> 0
# [0.00000080s] fib(1) -> 1
# [0.00003900s] fib(2) -> 1
# [0.00000050s] fib(1) -> 1
# [0.00000090s] fib(0) -> 0
# [0.00000080s] fib(1) -> 1
# [0.00002910s] fib(2) -> 1
# [0.00005410s] fib(3) -> 2
# [0.00011550s] fib(4) -> 3
# [0.00000050s] fib(1) -> 1
# [0.00000050s] fib(0) -> 0
# [0.00000050s] fib(1) -> 1
# [0.00002120s] fib(2) -> 1
# [0.00004220s] fib(3) -> 2
# [0.00000050s] fib(0) -> 0
# [0.00000060s] fib(1) -> 1
# [0.00002110s] fib(2) -> 1
# [0.00000040s] fib(1) -> 1
# [0.00000050s] fib(0) -> 0
# [0.00000060s] fib(1) -> 1
# [0.00002170s] fib(2) -> 1
# [0.00004200s] fib(3) -> 2
# [0.00008290s] fib(4) -> 3
# [0.00014540s] fib(5) -> 5
# [0.00028300s] fib(6) -> 8

print("-"*20,'使用functools.cache做函数备忘——使用caceh后','-'*20)
@functools.cache
@clock
def fibwithcache(n):
    return n if n < 2 else fibwithcache(n-2) + fibwithcache(n-1)

print(fibwithcache(6))
# 输出
# [0.00000080s] fibwithcache(0) -> 0
# [0.00000060s] fibwithcache(1) -> 1
# [0.00003700s] fibwithcache(2) -> 1
# [0.00000120s] fibwithcache(3) -> 2
# [0.00005970s] fibwithcache(4) -> 3
# [0.00000090s] fibwithcache(5) -> 5
# [0.00008160s] fibwithcache(6) -> 8

# 对比使用了functools.cache后可以明显看到，节省了大量的重复计算，这就是cache备忘的作用，同时也使得计算过程更加省时间
# 注意到是在原来的@clock的基础上，又在上层添加了@functools.cache装饰器
# 多个装饰器就像一个嵌套调用的过程，外层装饰器装饰的是内层装饰过的函数
# 使用cache的前提是，被装饰的函数的入参必须是可哈希的，因为cache的底层调用的是lur_cache，而lur_cache使用的dict存储的结果