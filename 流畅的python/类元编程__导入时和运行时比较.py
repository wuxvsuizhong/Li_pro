from builderlib import Builder,deco,Descriptor

print('# evaldemo mudile start')

@deco
class Klass(Builder):
    print('# Klass body')

    attr = Descriptor() # attr是描述符类Descriptor的实例化

    def __init__(self):
        super().__init__()
        print(f'# klass.__init__({self!r})')

    def __repr__(self):
        return '<Klass instance>'

def main():
    obj = Klass()
    obj.method_a()
    obj.method_b()
    obj.attr = 999


if __name__ == '__main__':
    main()

print('# evaldemo mudule end')

# 打印如下
# @ Builderlib module start
# @ Builder body
# @ Descriptor body
# @ Builderlib mudule end   ---------------到这里为止，都是导入的时候执行的
# # evaldemo mudile start   ---------------本模块开始执行的
# # Klass body
# @ Descriptor.__init__(<Descriptor instance>)  -------进入到描述符类Descriptor
# @ Descriptor.__set_name__((<Descriptor instance>, <class '__main__.Klass'>, 'attr'))      ------调用描述符类的__set_name__
# @ Builder.__init_subclass__(<class '__main__.Klass'>)     --------调用Klass的超类Builder的__init_subclass__
# @ deco(<class '__main__.Klass'>   --------应用deco类装饰器
# @ Builder.__init__(<Klass instance>   --------由Builder的__init__中，super().__init__触发，执行超类的__init__，
# # klass.__init__(<Klass instance>)    --------Builder的__init__触发
# @ SuperA.__init_subclass__:inner_0(<Klass instance>)
# @ deco:inner_1(<Klass instance>
# @ Dessciptor.__set__(<Descriptor instance>, <Klass instance>, 999)
# # evaldemo mudule end

# 从打印上可以看出来，其实被导入的模块中的一些全局信息是最先执行的
# 然后是本模块的全局信息
# 再然后就是本模块类实例化时，先是类变量的执行，然后是描述符的实例化
# 然后是超类的__init_subclass__，本模块的类装饰器
# 再然后是本模块中类的__init__，最后才是本模块中的方法调用，参数赋值等
