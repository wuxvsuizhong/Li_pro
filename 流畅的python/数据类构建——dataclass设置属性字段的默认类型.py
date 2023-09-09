from dataclasses import dataclass,field

# 使用dataclass装饰器会自动生成__init__方法，自动调用__init__把标注了注解的字段在后续的实例构建时抓换为实例属性，

@dataclass
class ClubMember:
    name:str
    # guest:list = [] #不能添加可变的类型为属性的默认值
    guest:list = field(default_factory=list)    #使用default_factory参数指定工厂方法，工厂方法可以是一个函数,类，或者其他的可调用对象
    # 指定了工程方法以后，在每次创建数据类的实例的时候调用(不带参数），构建默认值

c1 = ClubMember("张三")   #传递一个值最为name属性，那么guest熟就使用默认的list方法构建为一个列表
print(c1.name,c1.guest)  # 张三 []

# 更加准确的属性类型
@dataclass
class ClubClass2:
    name:str
    # 注解使用的list中的元素为字符串str（但是py不检验类型，即使传递其他的类型也不报错，限定list[str]更像是一种君子协定）
    guest:list[str] = field(default_factory=list)

c2 = ClubClass2("张三")
print(c2.name,c2.guest)

# field参数限定字段默认值的各种属性
@dataclass
class ClubClass3:
    name:str
    guest:list = field(default_factory=list)
    athlete:bool = field(default = False,repr=False)  #default设置字段的默认值，repe赋值为False表示不提供athlete字段给__repr__调用
c3 = ClubClass3("张三")
print(c2.name,c2.guest,c3.athlete)

##############################
# 上述dataclass会自动调用生成的__init__把字段设置为实例属性，但是入股需要一些__init__之后的工作，就需要定义__post_init__方法
# 定义了__post_init__方法后，它会被自动调用，去做一些__init__之后的事情
##############################
from typing import ClassVar
@dataclass
class HackClubMember(ClubMember):
    # all_handles = set()     # 类属性all_handles
    all_handles : ClassVar[set[str]] = set()   # 为了使得mypy检查工具满意，注解使用ClassVar
    # ClassVar有两个作用：1.不为属性在构建实例时生成实例字段，也就是仍然限定字段为类属性
    #                   2.表述其默认是一个空的集合set().并且集合中存放的str字符串，也就是[set[str]]这一段的表述
    handle :str=''          # 带有注解的，在构建后将被设置为实例属性

    def __post_init__(self):
        cls = self.__class__
        if self.handle =='':
            # 如果没有传入handle,那么设置handle为name的首段字符串
            self.handle = self.name.split()[0]
        if self.handle in cls.all_handles:
            # 如果handle有重复那么抛出ValueError
            msg = f'handle {self.handle!r} already exists!'
            raise ValueError(msg)
        cls.all_handles.add(self.handle)

anna = HackClubMember("Anna Revne",handle='AnnaReven')
print(anna)
leo = HackClubMember("Leo Rocheal")     #没传递handle，那么handle会在__post_init__中被设置为Leo
print(leo)
print(leo.__doc__)
leo2 = HackClubMember("Leo VaCinci")  # error handle为Leo的已经存在了
print(leo2)