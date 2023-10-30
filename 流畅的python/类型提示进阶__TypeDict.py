from typing import TypedDict

class BookDict(TypedDict):
    isbn : str
    title : str
    authors: list[str]
    pagecount: int

# TypeDict有一下两个作用
# 1. 使用和类相似的结构，为各个字段的值类型提供类型提示
# 2.通过一个构造函数告诉类型检查工具，字典应该具有的键值和指定类型的值

# 可以像dict构造函数那样调用BookDict,传入挂念自参数，也可以传一个包含字典字面量的字典参数
# TypeDict中注解类型并不是强制的，拨入这里的authors奔雷注解的类型是字符串列表，但是这里传入字符串，运行时也不会报错
pp = BookDict(title='Progremming Pears',authors='Joh',isbn='821231232',pagecount=256)

# pp是调用BookDict产生的一个数据体，结果是一个普通的字典类型
print(pp)   # {'title': 'Progremming Pears', 'authors': 'Joh', 'isbn': '821231232', 'pagecount': 256}
print(type(pp)) #<class 'dict'>
# pp.title  接上文，pp是一个普通字典，左右不能用"."操作符访问，会报错 AttributeError: 'dict' object has no attribute 'title'
print(pp['title'])  # Progremming Pears pp是一个字典，用[]访问
print(BookDict.__annotations__) # {'isbn': <class 'str'>, 'title': <class 'str'>, 'authors': list[str], 'pagecount': <class 'int'>} 类型提示在BookDict.__annotations__中

# ·
