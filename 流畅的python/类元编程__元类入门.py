class MetaBunch(type): # 继承type，创建新的元类
    def __new__(meta_cls,cls_name,bases,cls_dict):  # 第一个参数实际上和self一样，剩下的参数和直接使用type创建类时传递的参数是一样的
        defaults = {}

        def __init__(self,**kwargs):
            for name,default in defaults.items():
                setattr(self,name,kwargs.pop(name,default))
            if kwargs:
                extra = ', '.join(kwargs)
                raise AttributeError(f'No slots left for: {extra}')

        def __repr__(self):
            rep = ', '.join(f'{name}={value!r}' for name,default in defaults.items()
                            if(value := getattr(self,name))!= default)
            return f'{cls_name}({rep})'

        new_dict = dict(__slots__=[],__init__=__init__,__repr__ = __repr__)

        for name,value in cls_dict.items():
            if name.startswith('__') and name.endswith('__'):
                if name in new_dict:    # 禁止覆盖已有的__slots__,__init__等属性
                    raise AttributeError(f"can't set {name!r} in {cls_name}")
                new_dict[name] = value  # 新的以双下划线开头和结尾的属性，添加到new_dict中
            else:
                new_dict['__slots__'].append(name)  #如果不是双下划线开头和结尾的属性，加入到__slots__
                defaults[name] = value  # 并在default字典中添加键值对

        # print(meta_cls.__mro__) # (<class '__main__.MetaBunch'>, <class 'type'>, <class 'object'>)
        return super().__new__(meta_cls,cls_name,bases,new_dict)    # MetaBunch的直接超类其实就是type
        # 这里调用超类也就是type创建新的类，然后返回（注意是新的类返回不是具体的实例）

class Bunch(metaclass = MetaBunch):
    pass
# 设置Bunch的元类为MetaBunch



class Point(Bunch):
    x = 0.0
    y = 0.0
    color = 'gray'

if __name__ == "__main__":
    Point(x=1.2,y=3,color='green')
    p = Point()
    print(p.x,p.y,p.color)  # 0.0 0.0 gray
    print(f'{p!r}') # Point()

    # Point(x=1,y=3,z=3)  # AttributeError: No slots left for: z 因为在MetaBun中设置了__slots__，那么就不能设置__slots__没有包含的属性

# #############
# 元类求解时间实验
# #############
from builderlib import Builder,deco,Descriptor
from metalib import MetaKlass

print('# evaldemo_meta module start')

@deco
class Klass(Builder,metaclass=MetaKlass):
    print('# Klass body')
    attr = Descriptor()

    def __init__(self):
        super().__init__()
        print(f'# Klass.__init__({self!r})')

    def __repr__(self):
        return '<Klass instance>'


if __name__ == "__main__":
    print('-'*20,'元类求解时间实验','-'*20)
    obj = Klass()
    obj.method_a()
    obj.method_b()
    obj.method_c()
    obj.attr = 999

print('# evaldemo_meta module end')

