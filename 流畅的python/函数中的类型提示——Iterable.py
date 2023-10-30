from collections.abc import Iterable

# 根据提供的映射map,批量替换字符串中的字符

FromTo = tuple[str,str]     # FromTo 是一个类型别名
def zip_replace(text:str,changes:Iterable[FromTo]) -> str:
    for from_,to in changes:
        text = text.replace(from_,to)
    return text

l33t = [('a','4'),('e','3'),('i','1'),('o','0')]
text = 'mad skilled noob powned leey'
print(zip_replace(text,l33t))   #m4d sk1ll3d n00b p0wn3d l33y

# Iterable 最适合注解参数的类型，用来注解返回值的话则太过含糊，函数的返回值类型应该具体，明确
# 这个栗子中使用了类型别名 FromTo = tuple[str,str]，类型别名也可以通过TypeAlias定义

# 类型别名
from typing import TypeAlias
FromTo: TypeAlias = tuple[str,str]