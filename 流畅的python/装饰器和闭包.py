# 装饰器通常会把一个函数替换成另外一个函数

def deco(func):
    def inner():
        print('running inner()')
    return inner    # 返回内部函数的引用

@deco
def target():
    print('runing target()')

target()    #running inner()
print(target)   #<function deco.<locals>.inner at 0x000001E5658B9DA0>

# 何时执行装饰器
registry = []

def register(func):
    print(f'running register({func})')
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')

@register
def f2():
    print('running f2()')

def f3():
    print('runing f3()')

def main():
    print('runing main()')
    print('registry ->',registry)
    f1()
    f2()
    f3()

if "__main__" == __name__:
    main()
# 运行结果如下：
# running register(<function f1 at 0x0000020685109E40>)
# running register(<function f2 at 0x0000020685109EE0>)     # 装饰函数先于main函数执行
# runing main()     # main函数后于装饰函数执行
# registry -> [<function f1 at 0x0000020685109E40>, <function f2 at 0x0000020685109EE0>]
# running f1()
# running f2()
# runing f3()

# 装饰器在导入模块时立即执行，被装饰函数只在显示调用时运行吗=