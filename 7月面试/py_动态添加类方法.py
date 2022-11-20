class Person(object):
    def __init__(self,name):
        self.name = name

    def get_name(self):
        print(self.name)


p=Person('abc')
p.get_name()

@classmethod
def count(cls, count_num=None):
    if not hasattr(cls,"count_num"):   #判断类cls中是否有count_num这个属性
        cls.count_num=0
    else:
        cls.count_num += 1
    
    print('count_num=%d' % cls.count_num)

Person.count = count

p.count()
p.count()

p2=Person('dfr')
p2.count()
