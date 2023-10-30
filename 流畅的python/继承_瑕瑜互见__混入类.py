# ##############################################
# 一个混入类的例子——使用混入类实现一个不区分大小写的映射
# ##############################################
import collections
def _upper(key):
    try:
        return key.upper()
    except AttributeError:
        return key

class UppeCaseMixin:
    def __setitem__(self, key, value):
        super().__setitem__(_upper(key),value)

    def __getitem__(self, key):
        return super().__getitem__(_upper(key))

    def get(self,key,default = None):
        return super().get(_upper(key),default)

    def __contains__(self, key):
        return super().__contains__(_upper(key))


class UpperDict(UppeCaseMixin,collections.UserDict):
    pass

class UpperCounter(UppeCaseMixin,collections.Counter):
    """一个特殊的计数器，字符串键是大写形式"""

d = UpperDict([('a','letter A'),(2,'digit two')])
print(list(d.keys()))   # ['A', 2]
d['b'] = 'letter B'
print('b' in d) # True
print(d['a'],d.get('B'))    # letter A letter B
print(list(d.keys()))       # ['A', 2, 'B']

c = UpperCounter('BaNanA')
print(c.most_common())  # [('A', 3), ('N', 2), ('B', 1)]

# 混入类的强大之处在于，他可以添加一个功能扩展类，这个类里面集合了各种扩展方法，通过多重继承，把并列继承的超类方法进行遮盖
# 同时还可以再遮盖并列超类的同时，额外增加功能，这样相比传统的继承的优势在于，传统继承从原始的超类一路下来，中间可能继承很多中代需要但是后代不需要的方法
# 使用混入类继承就可以从一定程度上灵活的继承扩展

