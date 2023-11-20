import sys
# ############
# 上下文管理器类
# ############

class LookingClass:
    """LookingClass的作用是临时把打印反转"""
    def __enter__(self):
        self.original_write = sys.stdout.write  # 备份原来的打印
        sys.stdout.write = self.reverse_write   # 指定打印方式为自定义的打印
        return 'JABBERWOCKY'

    def reverse_write(self,text):
        """设置自定义的打印方式为反转字符串"""
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.write = self.original_write  # 恢复到系统原来的打印方式
        if exc_type is ZeroDivisionError:
            print('请不要除0')
            return True

if __name__ == "__main__":
    with LookingClass() as what:
        print('A B and C')  # C dna B A
        print(what)     # YKCOWREBBAJ   这里的打印说明with ... as ...语句，调用山下文后as后的对象绑定的是__enter__中返回return的值

    print(what) #JABBERWOCKY
    print('恢复正常~')

    manager = LookingClass()
    print(manager)  # <__main__.LookingClass object at 0x00000266A5D80990>

    monster = manager.__enter__()
    print(monster)  # YKCOWREBBAJ
    monster = 'ABCDEF'
    print(monster)  # FEDCBA
    print(manager)  # >01A0AB330A100000x0 ta tcejbo ssalCgnikooL.__niam__< 因为此时已经进入了manager也就是LookingClass的上下文中了，所以这时候的所有的打印都是反转的
    manager.__exit__(None,None,None) # 调用上下文的__exit__方法退出上下文，传递的三个参数exc_type,exc_val,exc_tb 传None
    print(monster)  # ABCDEF 退回上下文后，打印恢复正常

# #################
# 使用contextmanager
# #################
import contextlib
import sys

@contextlib.contextmanager
def looking_glass():
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    yield 'JABBEWRWOCKY'    # yield前面的语句相当于__enter__中的语句，yield语句本身就是相当于__enter__中的return
    sys.stdout.write = original_write   # yield后面的语句，相当于是__exit__中的语句

if __name__ == "__main__":
    print('-'*10,"使用contextlib.contextmanager",'-'*10)
    with looking_glass() as what:
        print('A B and C')  # C dna B A
        print(what) # YKCOWRWEBBAJ

    print(what) # JABBEWRWOCKY  退出上下文管理器后，回复正常
    print("恢复正常~")

# contextlib.contextmanager 这个装饰器的作用就是快捷的实现一个上下文管理器，不需要在编写一个上下文管理器类
# 只需要实现一个含有yield语句的生成器集即可，用啦生成想让__enter__返回的值
# yield把函数分为两个部分，yield前面的所有代码在with块开始的时候(解释器调用__enter__方法时)执行，yield后面的代码在with结束时(调用__exit__方法时)执行
# 简而言之，contextmanager装饰器就是把函数,包装成了实现__enter__和__exit__方法的上下文管理器类

# 目前这个looking_glass上下文管理器没有把异常纳入管理，接下来添加异常处理

@contextlib.contextmanager
def looking_glass():
    original_write = sys.stdout.write
    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''
    try:
        yield 'JABBEWRWOCKY'
    except ZeroDivisionError:
        msg = '请不要除0操作'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)

# 这里只是以ZeroDivisionError异常处理的为例，实际运用时候，会有其他的异常类
# 要把yield语句放在try/finally语句中，因为具体在使用上下文管理器时无法断定实际会有什么异常

# ########################################
# contextmanager装饰的上下文管理器可以用作装饰器
# ########################################
@looking_glass()    # 注意这里要加上()调用，因为只有调用后才会有返回上下文管理器实例
def verse():
    print('正常的顺序')

verse() # 序顺的常正
print("测试恢复正常")
