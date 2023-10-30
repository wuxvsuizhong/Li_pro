from collections.abc import Sequence
from random import shuffle
from typing import TypeVar

T = TypeVar('T')


def sample(population: Sequence[T], size: int) -> list[T]:
    if size < 1:
        raise ValueError('size must be >=1')
    result = list(population)
    shuffle(result)
    return result[:size]


print(sample([1, 2, 3, 4, 5, 6, 7], 2))
print(sample('abcdefg', 2))
print(sample([1, 2, 3, 4, 5, 6, 7, 'abcdefgh'], 3))

from collections import Counter
from collections.abc import Iterable
def mode(data:Iterable[float]) ->float:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]

print(mode([1,1,2,3,3,3,3,4]))

# 受限的typeVar
from collections.abc import Iterable
from decimal import Decimal
from fractions import Fraction
from typing import TypeVar

# 用NumerT这个类型别名来替代 float,Decimal,Fraction
NumberT = TypeVar('NumberT',float,Decimal,Fraction)
# def mode2(data:Iterable[NumberT]) -> NumberT:
#     pass

# 从此处可以看出，TypeVar可以映射为多个类型，但是，一般是基础类型是同一种的才这样用
# 如果是 NumberT = TypeVar('NumberT',float,Decimal,Fraction，str) 这种，str明显不和其他几种是同一类，用TypeVar就显得不合适了，于是使用有界的TypeVar
from collections import Counter
from collections.abc import Iterable,Hashable
from typing import TypeVar

HashableT = TypeVar('HashableT',bound=Hashable)

def mode3(data:Iterable[HashableT]) ->HashableT:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]

print(mode3([[1,1,2,3],3,3,3,4]))   # error,子列表是不可哈希的


