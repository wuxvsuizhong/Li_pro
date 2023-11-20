from typing import Callable,Any,get_type_hints,NoReturn
class Field:
    """描述符类Field"""
    def __init__(self,name:str,constructor:Callable)->None:
        if not callable(constructor) or constructor is type(None):
            raise TypeError(f'{name!r} type hint must be callable')
        self.name = name
        self.storage_name = '_'+name
        self.constructor = constructor

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance,self.storage_name)

    def __set__(self, instance:Any, value:Any)->None:
        if value is ...:
            value = self.constructor()
        else:
            try:
                value = self.constructor(value)
            except (TypeError,ValueError) as e:
                type_name = self.constructor.__name__
                msg = f'{value!r} is not comptible with{self.name}:{type_name}'
                raise TypeError(msg) from e
        setattr(instance,self.storage_name,value)

class CheckedMeta(type):
    def __new__(meta_cls, cls_name, bases,cls_dict):
        print(f"in CheckedMeta，cls_name:{cls_name},bases:{bases},cls_dict:{cls_dict}")
        if '__slots__' not in cls_dict:
            print(f'when cls_name={cls_name},running checkedMeta __new__。。。')
            slots = []
            type_hints = cls_dict.get('__annotations__',{})
            for name,constructor in type_hints.items():
                field = Field(name,constructor)
                cls_dict[name] = field
                slots.append(field.storage_name)

            cls_dict['__slots__'] = slots

        return super().__new__(meta_cls,cls_name,bases,cls_dict)

class Checked(metaclass=CheckedMeta):
    __slots__ = ()  # Checked类，这里有了__slots__，所以元类CheckedMeta的__new__中的if条件不会执行

    @classmethod
    def _fields(cls)->dict[str,type]:
        return get_type_hints(cls)

    def __init__(self,**kwargs:Any)->None:
        for name in self._fields():
            value = kwargs.pop(name,...)
            setattr(self,name,value)
        if kwargs:
            self.__flag_unkown_attrs(*kwargs)

    def __flag_unkown_attrs(self,*names:str)->NoReturn:
        plural = 's' if len(names) > 1 else ''
        extra = ', '.join(f'{name!r}' for name in names)
        cls_name = repr(self.__class__.__name__)
        raise AttributeError(f'{cls_name} object has no attribute {plural} {extra}')
    def _asdict(self)->dict[str,Any]:
        return {
            name:getattr(self,name) for name,attr in self.__class__.__dict__.items()
            if isinstance(attr,Field)
        }

    def __repr__(self):
        kwargs = ', '.join(f'{key}={value!r}' for key,value in self._asdict().items())
        return f'{self.__class__.__name__}({kwargs})'


class Movie(Checked):
    title:str
    year:int
    box_office:float

# 和使用__init_subclass__方法相比，使用元类CheckedMeta，用元类的__new__方法，替代__init_subclass__
# 实现了自己的__slots__,那么除了__slots__中包含的属性，不能再添加其他的属性，这就去掉了__setattr__方法

if __name__ == "__main__":
    movie = Movie(title="ABX",year=2023,box_office=137)
    # in CheckedMeta，cls_name:Checked,bases:(),cls_dict:{'__module__': '__main__', '__qualname__': 'Checked', '__slots__': (), '_fields': <classmethod(<function Checked._fields at 0x000001ED6B7AD6C0>)>, '__init__': <function Checked.__init__ at 0x000001ED6B7AD760>, '_Checked__flag_unkown_attrs': <function Checked.__flag_unkown_attrs at 0x000001ED6B7AD800>, '_asdict': <function Checked._asdict at 0x000001ED6B7AD8A0>, '__repr__': <function Checked.__repr__ at 0x000001ED6B7AD940>}
    # in CheckedMeta，cls_name:Movie,bases:(<class '__main__.Checked'>,),cls_dict:{'__module__': '__main__', '__qualname__': 'Movie', '__annotations__': {'title': <class 'str'>, 'year': <class 'int'>, 'box_office': <class 'float'>}}
    # when cls_name=Movie,running checkedMeta __new__。。。
    # 可以看到，这里调用了两次的CheckedMeta的__new__，一次是Checked类，一次是Movie类,只不过Checked类没有__slots__所以没有执行__new__方法的if判断，第二次Movie类没有__slots__，所以执行了__new__里面的if判断语句

    print(movie)    # Movie(title='ABX', year=2023, box_office=137.0)
    print(movie.year)   # 2023
    print(Movie.year)   # <__main__.Field object at 0x00000232BE6867D0> 实例化对象movie的属性是Field描述符类的实例化对象
    print(movie.__class__)  # <class '__main__.Movie'>  实例化对象movie,是类Movie的实例化
    print(Movie.__class__)  # <class '__main__.CheckedMeta'>    Movie类对象，是ChekedMeta的实例化

    print(Movie.__bases__)  # (<class '__main__.Checked'>,)
    # movie.box_office = 'IIIT'   # TypeError: 'IIIT' is not comptible withbox_office:float
    # movie.z = 100
