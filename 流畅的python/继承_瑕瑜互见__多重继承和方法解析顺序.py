# ################################################
# 菱形继承的例子——super()不是简单的调用父类的方法而已
# ################################################
class Root:
    def ping(self):
        print(f'{self}.ping() in Root')

    def pong(self):
        print(f'{self}.pong() in Root')

    def __repr__(self):
        cls_name = type(self).__name__
        return f'<instance of {cls_name}>'

class A(Root):
    def ping(self):
        print(f'{self}.ping() in A')
        super().ping()

    def pong(self):
        print(f'{self}.pong in A')
        super().pong()

class B(Root):
    def ping(self):
        print(f'{self}.ping() in B')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in B')


class Leaf(A,B):
    def ping(self):
        print(f'{self}.ping() in Leaf')
        super().ping()


leaf1 = Leaf()
leaf1.ping()
# <instance of Leaf>.ping() in Leaf
# <instance of Leaf>.ping() in A
# <instance of Leaf>.ping() in B     Leaf继承了A,B，根据继承的顺序，Leaf唤醒父类的ping()
# <instance of Leaf>.ping() in Root     Leaf的超类A,B的ping方法都再次向上唤醒Root.ping，但是Root.ping只被唤醒一次

leaf1.pong()
# Leaf本身并没有pong方法，他是调用的超类A,B中的pong方法
# <instance of Leaf>.pong in A  唤醒A的pong方法，但是不会在超类A中向上唤醒Root.pong
# <instance of Leaf>.pong() in B    唤醒B的pong方法，但是不会在超类A中向上唤醒Root.pong

# Leaf同时继承了A,B, 而A,B共同继承自Root
# 思考如下问题：
# 为什么Leaf.ping可以同时唤醒 A.ping和B.ping，但是再向上只能唤醒一次的Root.Ping？
# Leaf调用超类A,B的pong方法，其中B.pong没有调用super，但是A.pong有调用super,但是最终Leaf.pong没有从A.pong的super调用到Root.pong?

print(Leaf.__mro__) #(<class '__main__.Leaf'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Root'>, <class 'object'>)

# 每个类都有一个__mro_-的属性，按照方法解析顺序列出各个超类，顺序从当前类一直到object类
# 方法解析顺序决定唤醒顺序，置于各个类的响应的类是否被唤醒，取决于实现时是否调用super()
# 调用super()的方法被称为协作方法，使用协作方法可以实现协作多重继承
# 解答上面的疑问，因为方法唤醒的顺序按照__mro__列数的类顺序来的，所以Leef.ping->A.ping->B.ping->Root.ping
# 而Leaf本身没有pong，所以按照顺序唤醒A.pong->B.pong 但是 B.pong没有super调用，所以调用链从此处终止

# #######################
# super的动态行为
# #######################
class U():
    def ping(self):
        print(f'{self}.ping() in U')
        super().ping()

class LeafUA(U,A):
    def ping(self):
        print(f'{self}.ping() in LeafUA')
        super().ping()

u = U()
# u.ping()  # U的超类中没有哪个类实现ping，在super().ping调用会出错
#     super().ping()
#     ^^^^^^^^^^^^
# AttributeError: 'super' object has no attribute 'ping'

leaf2 = LeafUA()
leaf2.ping()
# <instance of LeafUA>.ping() in LeafUA
# <instance of LeafUA>.ping() in U
# <instance of LeafUA>.ping() in A
# <instance of LeafUA>.ping() in Root

print(LeafUA.__mro__)   # (<class '__main__.LeafUA'>, <class '__main__.U'>, <class '__main__.A'>, <class '__main__.Root'>, <class 'object'>)

# LeafUA同时集成了U,A，但是在LeafUA.ping中，调用了super().ping,所以唤醒顺序为LeafUA.ping->U.ping->A.ping->Root.ping
# 虽然单独的U.ping中，super.ping会报错，但是如果U被继承，在U.ping中的super().ping 确是可以唤醒在__mro__属性中临近的超类方法

class LeafAU(A,U):
    def ping(self):
        print(f'{self}.ping() in LeafAU')
        super().ping()

leaf3 = LeafAU()
leaf3.ping()
# <instance of LeafAU>.ping() in LeafAU
# <instance of LeafAU>.ping() in A
# <instance of LeafAU>.ping() in Root
print(LeafAU.__mro__) #(<class '__main__.LeafAU'>, <class '__main__.A'>, <class '__main__.Root'>, <class '__main__.U'>, <class 'object'>)
# LeafAU的同时继承 A和U，但是和LeafUA的区别是后者继承顺序是U,A
# 所以唤醒顺序为Leaf.ping->A.ping->Root.ping 因为从A直接到达了顶层的Root，Root后没有Super方法，座椅调用链到这里终止，不会调用到U.ping