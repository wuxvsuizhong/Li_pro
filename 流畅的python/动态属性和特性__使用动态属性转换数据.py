import keyword
from collections import abc

class FrozenJSON:
    def __init__(self,mapping):
        # self.__data = dict(mapping)     # __data前面有两个下划线。是私有属性
        self.__data = {}
        for key,val in mapping.items():
            if keyword.iskeyword(key):  # 用keyword模块的iskeyword方法判断是否存在和关键字相同的字段
                key += '_'  # 如果是和内置关键字相同的字段，那么给字段加一个下划线后缀
            self.__data[key]= val

    def __getattr__(self, name):    # 当在FrozenJSON中没有获取到属性name的时候，才会调用__getattr__方法
        try:    # 如果name匹配__data中的某个属性，就返回对应的属性
            return getattr(self.__data,name)
        except AttributeError:  # 如果从__data这个map中获取某个key
            return FrozenJSON.build(self.__data[name])

    def __dir__(self):
        return self.__data.keys()
    @classmethod
    def build(cls,obj):
        if isinstance(obj,abc.Mapping):
            return cls(obj)
        elif isinstance(obj,abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj

import json
if __name__ == "__main__":
    raw_feed = json.load(open("./osconfeed.json"))
    feed = FrozenJSON(raw_feed)

    print(feed.keys())  # dict_keys(['Schedule'])   feed实际上是一个经过json序列化后的py字段，最外层只有一个键Schedule
    print(len(feed.Schedule.speakers))  # 357
    print(sorted(feed.Schedule.keys())) # ['conferences', 'events', 'speakers', 'venues']   在Schedule这个键对应有下一级的4个键'conferences', 'events', 'speakers', 'venues'
    for key,val in sorted(feed.Schedule.items()):
        print(f'{len(val):3} {key}')    # 统计Schedule的子级下的键值对中，各个键值对饮的值的长度
        #   1 conferences
        # 484 events
        # 357 speakers
        #  53 venues

    print(feed.Schedule.speakers[-1].name)  # Carina C. Zona
    talk = feed.Schedule.events[40]
    print(type(talk))   # <class '__main__.FrozenJSON'>
    print(talk.name,talk.speakers)  # There *Will* Be Bugs [3471, 5199]

    print(talk.flavor)  # KeyError: 'flavor'

# 当使用"."操作，通过一级级的键值获取属性的时候，其实先会尝试在FrozenJSON中获取本身的实例或者类属性，当没有获取到的时候，就会排除

# #######################
# 使用__new__方法灵活创建对象
# #######################

# 首先要清楚一点，__new__方法是一个内置的类方法，以特殊方式对待，因此不需要使用@classmethod装饰器
# __new__方法创建会创建然后返回实例，在把这个实例传递给__init__的第一个参数self

class FrozenJson2:
    def __new__(cls,arg):   # __new__是一个类方法，注意第一个入参是cls
        if isinstance(cls,abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg,abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self,mapping):
        self.__data = {}
        for key,val in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = val

    def __getattr__(self, name):
        try:
            return getattr(self.__data,name)
        except AttributeError:
            return FrozenJson2(self.__data[name])

    def __dir__(self):
        return self.__data.keys()   # 在控制台或者是代码中使用dir(FrozenJson2)时，展示的属性列表




