class Money(object):
    def __init__(self):
        self.__money=0

    def setMoney(self,num):
        if isinstance(num,int):
            self.__money = num
        else:
            print("error")

    def getMoney(self):
        return self.__money

    money = property(getMoney,setMoney)

m=Money()
m.money=100
print(m.money)

m.money = 110.5
print(m.money)

print("=="*10)

class Money2(object):
    def __init__(self):
        self.__money = 0

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self,num):
        if isinstance(num,int):
            self.__money = num
        else:
            print('ERROR')


m2=Money2()
print(m2.money)
m2.money=100
print(m2.money)
m2.money=110.5
print(m2.money)
