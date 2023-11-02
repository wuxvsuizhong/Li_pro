# 不使用yield from时,如果约个生成器根据拎一个生成器产出值,需要使用for循环
def sub_gen():
    yield 1.1
    yield 1.2

def gen():
    yield 1
    for i in sub_gen():
        yield i
    yield 2
# gen()这个生策划更年期调用了sub_gen（）生成器
for x in gen():
    print(x)
    # 输出：
    # 1    执行行7
    # 1.1   调用sub_gen，执行行3
    # 1.2   调用sub_gen。执行行4
    # 2     返回gen，执行行10

# 使用yield from 实现
def gen():
    yield 1
    yield from sub_gen()
    yield 2

for x in gen():
    print(x)

# ##########################
# yield from获取子生成器的返回值
# ##########################
print('-'*10,'yield from获取子生成器的返回值','-'*10)

def sub_gen():
    yield 1.1
    yield 1.2
    return 'Done'

def gen():
    yield 1
    result = yield from sub_gen()
    print('<--',result)  # 如果不获取sub_gen的return的值，那么外部迭代获取项不会直接获取到sub_gen中return的值
    yield 2

for x in gen():
    print(x)
    # 1
    # 1.1
    # 1.2
    # <-- Done      sub_gen中return的Done返回值，被赋值给了result
    # 2
##########
# 实现chain
##########
print('-'*10,'实现chain','-'*10)

def chain(*iterable):
    for it in iterable:
        for i in it:
            yield i

s='ABC'
r = range(3)
print(list(chain(s,r))) # ['A', 'B', 'C', 0, 1, 2]

print('-'*10,'yield from 实现chain','-'*10)
def chaion(*iterable):
    for it in iterable:
        yield from it

print(list(chain(s,r))) # ['A', 'B', 'C', 0, 1, 2]

# ##########
# 遍历树状结构
# ##########
print('-'*10,'遍历树状结构','-'*10)

def tree(cls):
    yield cls.__name__

def display(cls):
    for cls_name in tree(cls):
        print(cls_name)

if __name__ == "__main__":
    display(BaseException)  #BaseException  只输出了传入的类名

def tree(cls):
    yield cls.__name__,0
    for sub_cls in cls.__subclasses__():
        yield sub_cls.__name__,1

def display(cls):
    for cls_name,level in tree(cls):
        indent = ' '*4*level    # 根据返回的level拼接缩进
        print(f'{indent}{cls_name}')
if __name__ == "__main__":
    display(BaseException)
    # BaseException
    #     BaseExceptionGroup
    #     Exception
    #     GeneratorExit
    #     KeyboardInterrupt
    #     SystemExit

print('-'*10)
def sub_tree(cls):
    for sub_cls in cls.__subclasses__():
        yield sub_cls.__name__,1

def tree(cls):
    yield cls.__name__,0
    yield from sub_tree(cls)

def display(cls):
    for cls_name,level in tree(cls):
        indent = ' '*4*level    # 根据返回的level拼接缩进
        print(f'{indent}{cls_name}')

if __name__ == "__main__":
    display(BaseException)

print('-'*10,'遍历更深层的树状结构','-'*10)
def sub_tree(cls):
    for sub_cls in cls.__subclasses__():
        yield sub_cls.__name__,1
        for sub_sub_cls in sub_cls.__subclasses__():
            yield sub_sub_cls.__name__,2

if __name__ == "__main__":
    display(BaseException)
# 输出：
#     BaseException
#     BaseExceptionGroup
#         ExceptionGroup
#     Exception
#         ArithmeticError
#         AssertionError
#         AttributeError
#         BufferError
#         EOFError
#         ImportError
#         LookupError
#         MemoryError
#         NameError
#         OSError
#         ReferenceError
#         RuntimeError
#         StopAsyncIteration
#         StopIteration
#         SyntaxError
#       SystemError
#         TypeError
#         ValueError
#         Warning
#         ExceptionGroup
#     GeneratorExit
#     KeyboardInterrupt
#     SystemExit

print('-'*10,'递归打印类的树状结构','-'*10)

def tree(cls,level = 0):
    yield cls.__name__,level
    for sub_cls in cls.__subclasses__():
        yield from tree(sub_cls,level+1)

def display(cls):
    for cls_name,level in tree(cls):
        indent = ' '*4*level
        print(f'{indent}{cls_name}')


if __name__ == "__main__":
    display(BaseException)



