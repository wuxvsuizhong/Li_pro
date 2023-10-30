from typing import Callable, NamedTuple, Sequence, Optional
from decimal import Decimal


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


# 定义Promotion类型
Promotion = Callable[[Order], Decimal]
promos: list[Promotion] = []


def promotion(promo: Promotion) -> Promotion:
    """promotion装饰器，把策略promo自动添加到promos中，然后原封不动的返回promo"""
    promos.append(promo)
    return promo


def best_promo(order: Order) -> Decimal:
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)


@promotion
def fidelity(order:Order)->Decimal:
    """为积分1000以上的顾客提供5%折扣"""
    if order.custumer.fidelity >= 1000:
        return order.total() * decimal('0.05')
    return Decimal(0)

@promotion
def bulk_item(order:Order)->Decimal:
    """单个商品数量为20个或以上时提供10%折扣"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total()*Decimal('0.1')
    return discount

# 这里通过䘝特殊的装饰器promotion，凡是使用了这个装饰器的函数，会被自动添加到全局列表promos中，用户计算最佳折扣
