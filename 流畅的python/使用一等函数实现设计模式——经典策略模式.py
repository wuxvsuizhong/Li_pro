from abc import ABC, abstractmethod
from collections.abc import Sequence
from decimal import Decimal
from typing import NamedTuple, Optional


# ###################
# 经典策略模式——类实现
# ##################

class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity


class Order(NamedTuple):
    custumer: Customer
    cart: Sequence['LineItem']
    promotion: Optional['Promotion'] = None

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total:{self.total():.2f} due{self.due():.2f}>'


class Promotion(ABC):  # 策略：抽象基类
    @abstractmethod
    def discount(self, order: Order) -> Decimal:
        '''返回折扣金额(正值)'''


class FidelityPromo(Promotion):
    """为积分1000或以上的顾客提供5%折扣"""

    def discount(self, order: Order) -> Decimal:
        rate = Decimal('0.05')
        if order.custumer.fidelity >= 1000:
            return order.total() * rate
        return Decimal(0)


class BulkItemPromotion(Promotion):
    """单个商品的数量为30或者以上时提供10%折扣"""

    def discount(self, order: Order) -> Decimal:
        discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * Decimal(0.1)
        return discount


class LargeOrderPrommo(Promotion):
    """订单中不同商品达到10个或以上时提供7%折扣"""

    def discount(self, order: Order) -> Decimal:
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * Decimal('0.07')
        return Decimal(0)


joe = Customer('Jhon Doe', 0)
ann = Customer('Ann Smith', 1000)  # 定义两个顾客，第一个顾客的积分为0，第二个顾客的积分为1000
cart = (LineItem('banana', 4, Decimal('.5')),  # 购物车中有3个商品
        LineItem('apple', 10, Decimal('1.5')),
        LineItem('watermalen', 5, Decimal(5))
        )
print(Order(joe, cart, FidelityPromo()))  # <Order total:42.00 due42.00>  FidelitPromo没有给joe提供折扣
print(Order(ann, cart, FidelityPromo()))  # <Order total:42.00 due39.90> 5%的折扣
banana_cart = (
    LineItem('banana', 30, Decimal('.5')),
    LineItem('apple', 10, Decimal('1.5'))
)
print(Order(joe, banana_cart, BulkItemPromotion()))  # <Order total:30.00 due28.50>
long_cart = tuple(
    LineItem(str(sku), 1, Decimal(1)) for sku in range(10)  # long_order中有10个商品，每个价格1块钱
)
print(Order(joe, long_cart, LargeOrderPrommo()))  # <Order total:10.00 due9.30>
print(Order(joe, cart, LargeOrderPrommo()))  # <Order total:42.00 due42.00>

# 每个具体的策略都继承自抽象类 Promotion
# 每一个具体的策略都是一个类，策略实例没有状态（没有实例属性),表现更像函数
# 在Order传递参数时直接传递折扣策略类

# ##################
# 使用函数实现的折扣策略
# ##################
print('-' * 20, '函数实现的策略模式', '-' * 20)
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Callable, NamedTuple


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    """购物车中的每个商品条目"""
    product: str
    quantity: int
    price: Decimal

    def total(self):
        return self.price * self.quantity


@dataclass(frozen=True)
class Order:
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional[Callable[['Order'], Decimal]] = None

    # 注解promotion是一个可调用类型，该可调用类型接受的参数只有一个Order类型，返回值是Decimal类型
    # 其实这个注解就是说明了promotion是一个接受Order入参，返回值是Decimal的可调用函数，对应下方的各个策略函数

    def total(self) -> Decimal:
        """计算购物车中的商品总价"""
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        """得到折扣后的结果"""
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(self)  # 这里的入参也是self，是因为各个策略函数的入参是Order类型
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} dus:{self.due():.2f}>'


# 各个折扣策略接受的都是Oeder类型的参数，通过Order获取顾客的积分，购物车商品等信息
def fidelity_promo(order: Order) -> Decimal:
    """为积分1000或以上的顾客提供5%折扣"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)


def bulk_item_promo(order: Order) -> Decimal:
    """单个商品数量20个以上提供10%折扣"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


def large_order_promo(order: Order) -> Decimal:
    """订单中不同商品的数量达到10个或以上提供7%折扣"""
    dustinct_items = {item.product for item in order.cart}
    if len(dustinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)


joe = Customer('john Doe', 0)
ann = Customer('Ann Smith', 1000)
cart = [
    LineItem('banana', 4, Decimal('.5')),
    LineItem('apple', 10, Decimal('1.5')),
    LineItem('watermalon', 5, Decimal(5)),
]
print(Order(joe, cart, fidelity_promo))
print(Order(ann, cart, fidelity_promo))
banana_cart = [LineItem('banana', 30, Decimal('.5')),
               LineItem('watermalon', 10, Decimal(1.5))]
print(Order(joe, banana_cart, bulk_item_promo))
long_cart = [LineItem(str(item_code), 1, Decimal(1)) for item_code in range(10)]
print(Order(joe, long_cart, large_order_promo))
print(Order(joe, cart, large_order_promo))

# 不同于第一种的各个策略是class,这里的折扣策略是一个个的单独的函数，并成为order的一个可调用属性
# 在Order传递参数的时候，直接传递折扣函数

# 选择最佳的折扣
print('-' * 20, '选择最佳折扣', '-' * 20)
promos = [fidelity_promo, bulk_item_promo, large_order_promo]


def best_promo(order: Order) -> Decimal:
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)  # 迭代各个折扣，选取最大的折扣


print(Order(joe, long_cart, best_promo))
print(Order(joe, banana_cart, best_promo))
print(Order(ann, cart, best_promo))

# 有一个不方便的地方就是，在要新增策略时，除了需要定义新的策略函数之外，还需要把函数加入到promos列表中

# 下面使用内省的全局命名空间自动构建promos列表
# #######################
# 使用全局命名空间，自动构建最佳折扣列表中的成员
# #######################
promos = [promo for name, promo in globals().items() if name.endswith('_promo') and name != 'best_promo']
# 获取以_promo结尾的函数名，添加进promos列表内

# globals().items() 获取全局空间中的函数原型列表


def best_promo(order: Order) -> Decimal:
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)  # 迭代各个折扣，选取最大的折扣


# #################################
# inspect模块获取函数对象构建最佳折扣列表
# #################################
import inspect

promos = [func for _, func in inspect.getmembers(__name__, inspect.isfunction)]
# inspect.getmembers用于获取对象的属性，这里获取的是本模块__name__的属性
# 具体获取那些属性可以通过第二个参数控制了，这里使用的是inspect.isfunction获取函数


def best_promo(order: Order) -> Decimal:
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)  # 迭代各个折扣，选取最大的折扣

