from dataclasses import dataclass,field,fields
from typing import Optional
from enum import Enum,auto
from datetime import date

class ResourceType(Enum):
    BOOK = auto()
    EBOOK = auto()
    VIDIO = auto()

@dataclass
class Resource:
    """描述媒体资源"""
    identifier: str
    title:str = '<untitled>'    #一旦某个字段设置了默认值，那么后续的字段都要设置默认值
    creator:list[str] = field(default_factory=list)
    date:Optional[date] = None   #date的值可以是一个data类型或者是None
    type:ResourceType = ResourceType.BOOK
    description:str=''
    language:str=''
    subjects:list[str] = field(default_factory=list)

    def __repr__(self):
        # 实现自定义的__repr__，在print时对输出进行格式化
        cls = self.__class__
        cls_name = cls.__name__
        indent = ' '*4
        res = [f'{cls_name}(']
        for f in fields(cls):
            value = getattr(self,f.name)
            res.append(f'{indent}{f.name} = {value!r}')

        res.append(')')
        return '\n'.join(res)



des = 'Improvind the design of exstsing code'
book = Resource('978-8-13','书籍标题',['作者1','作者2','作者3'],date(2023,9,11),ResourceType.BOOK,des,'CN','面向对象OOP')
print(book)


