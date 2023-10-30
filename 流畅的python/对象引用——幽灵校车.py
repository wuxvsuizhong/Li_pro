# ###############
# 类实例的深浅拷贝 #
# ###############
class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = passengers
        else:
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


import copy

bus1 = Bus(["alice", "Bill", "Calire", "David"])
bus2 = copy.copy(bus1)  # 类实例的浅拷贝
bus3 = copy.deepcopy(bus1)  # 类实例的深拷贝
print("id(bus1):", id(bus1))
print("id(bus2):", id(bus2))
print("id(bus3):", id(bus3))  # 三个Bus实例的id各不相同，不是同一个实例对象

print("id(bus1.passengers):", id(bus1.passengers))
print("id(bus1.passengers):",
      id(bus2.passengers))  # bus2是浅拷贝的bus1，实例虽然不是同一个，但是实例中的passenger是同一个list的标签，所以两个passengers的id是相同的
print("id(bus1.passengers):", id(bus3.passengers))  # bus2是设拷贝的，所以它的passengers是一份单独新的数据，id和bus1,,bus2不同

bus1.drop('Bill')
print("after bus1 drop Bill")
print("bus1.passengers", bus1.passengers)
print("bus2.passengers", bus2.passengers)  # bus1和bus2的passengers是同一分数据，所以bus1修改passenfers会反映到bus2
print("bus3.passengers", bus3.passengers)  # bus3的passengers是单独的一份数据，不受影响

# #########
# 循环引用 #
# ########
a = [10, 20]
b = [a, 30]
a.append(b)
print(a)    # [10, 20, [[...], 30]]
print(a[2])     #[[10, 20, [...]], 30]
c = copy.deepcopy(a)
print(c)    # [10, 20, [[...], 30]]
print(c[2])     #[[10, 20, [...]], 30]  deepcopy也会处理循环引用

# #########################
# 函数可能会修改传递的可变对象 #
# #########################
def f(a,b):
    a+=b
    return a

x,y = 1,2
print(f(x,y))   #3
print(x,y)      #1 2

a=[1,2]
b=[3,4]
print(f(a,b))   #[1, 2, 3, 4]
print(a,b)      #[1, 2, 3, 4] [3, 4] a被修改了

a=(10,20)
b=(30,40)
print(f(a,b))   #(10, 20, 30, 40)
print(a,b)      #(10, 20) (30, 40)  #a和b保持原样没有被修改

# 总结：当函数传递的是可变类型的数据，那么在函数中修改会作用到数据源上
#       如果纯涤的是不可变的数据那么，在函数中进行修改将会创建新的数据，而源数据保持不变

# ########################
# 函数使用可变对象带来的问题 #
# ########################
class HuntedBus:
    """诡异的校车乘客"""
    def __init__(self,passengers=[]):
        self.passengers = passengers

    def pick(self,name):
        self.passengers.append(name)

    def drop(self,name):
        self.passengers.remove(name)
print("-"*10,"on HuntedBus",'-'*10)
bus1 = HuntedBus(["Alice","Bill"])
print("bus1.passengers:",bus1.passengers)
print("bus1 pick Charlie and drop Alice")
bus1.pick("Charlie")
bus1.drop("Alice")
print(bus1.passengers)

bus2 = HuntedBus()
bus2.pick("Carrie")
print(bus2.passengers)

bus3 = HuntedBus()
print(bus3.passengers)  # 可怕，bus3没有搭载任何的乘客，但是搭上bus2的Carrie出现在了bus3
bus3.pick("Dave")
print(bus2.passengers)  # ['Carrie', 'Dave'],在bus3上车的Carrie出现在了bus2上
print("bus3.passengers is bus2.passengers:",bus3.passengers is bus2.passengers)  # True,bus2和bus3的passengers是同一个列表

# 总结：如果使用可变参数作为函数形参的默认值，那么，在实例化时如果指定了参数去覆盖默认值，就一切正常
#         如果是不传递参数，就使用函数的默认值，那么就会导致实例数据之间共享同一个可变对象数据，导致"幽林乘客“的问题

# ###########
# 消失的乘客 #
# ##########
class Twilightes:
    """让乘客消失的校车"""

    def __init__(self,passengers=None):
        if passengers is None:
            self.passengers = []    #当不传递passengers时，创建一个新的空列表
        else:
            self.passengers = passengers   # self.passengers作为一个标签指向了外部的passengers列表

    def pick(self,name):
        self.passengers.append(name)

    def drop(self,name):
        self.passengers.remove(name)
        
print("-"*10,"幽灵校车",'-'*10)
篮球队=['Sue','Tina','Maya','Diana','Pat']
校车 = Twilightes(篮球队)
校车.drop("Tina")
校车.drop("Pat")
print(篮球队)  #Tina和Pat从校车上下来后，消失在了篮球队列表中
# 因为校车中，__init__函数里，self.passengers = passengers这一句将类属性self.passengers指向了外部的篮球队列表
# 所以在校车上drop操作将会直接影响篮球队列表中的数据
# 正确的做法是，在__init__函数中重新创建一份传入的pssengers数据
class Twilightes:
    """安全的校车"""

    def __init__(self,passengers=None):
        if passengers is None:
            self.passengers = []    #当不传递passengers时，创建一个新的空列表
        else:
            self.passengers = list(passengers)   # 当传入的passengers有数据实体时，list构造一份单独的数据给self.passengers

    def pick(self,name):
        self.passengers.append(name)

    def drop(self,name):
        self.passengers.remove(name)
print("-"*10,"安全的校车",'-'*10)
篮球队=['Sue','Tina','Maya','Diana','Pat']
安全的校车 = Twilightes(篮球队)
安全的校车.drop("Tina")
安全的校车.drop("Pat")
print(篮球队)  # Tina和Pat从校车上下来后，篮球队列表仍然正常