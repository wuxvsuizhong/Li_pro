from collections.abc import Iterable,Iterator
from typing import TypeVar,Protocol,Any

# SupportsLessThan继承自Protocal(协议） ，定义了一个协议——支持__lt__方法
# 也就是说只要类型T实现了__lt__的对象，都可以与协议SupportsLessThan相容
class SupportsLessThan(Protocol):
    def __lt__(self, other:Any) -> bool:...


LT = TypeVar('LT',bound=SupportsLessThan)   # 类型LT指代的SupportsLessThan 类型，而SupportsLessThan类型是一个协议
# 这样也就是实现了类型LT,去指代所有的实现了__lt__方法的类型

def top(series:Iterable[LT],length:int) -> list[LT]:
    ordered = sorted(series,reverse=True)
    return ordered[:length]

from typing import TYPE_CHECKING
import pytest

def test_top_tuples() -> None:
    fruit = 'mango pear apple kiwi banana'.split()
    series: Iterable[tuple[int,str]] = ((len(s),s) for s in fruit)
    length = 3
    expected = [(6,'banana'),(5,'momgo'),(5,'apple')]
    result = top(series,length)
    if TYPE_CHECKING:
        reveal_type(series)
        reveal_type(expected)
        reveal_type(result)

    # assert result == expected

    # 有意测试类型错误
    def test_top_objects_error() ->None:
        series = [object for _ in range(4)]
        if TYPE_CHECKING:
            reveal_type(series)
        with pytest.raises(TypeError) as excinfo:
            top(series,4)   # error: Value of type variable "LT" of "top" cannot be "type[object]"  [type-var]

        assert "'<' not support" in str(excinfo.value)

# 38行的会被mypy检查出错误，因为top函数的第一个参数是需要由LT类型的元素组成的Iterable对象，但是series是有object组成的列表，object没有实现__lt__方法，所以不是LT类型

# 定义一个实现了__lt__的类
class Spam:
    def __init__(self,n): self.n = n
    def __lt__(self, other):return self.n < other.n
    def __repr__(self):return f'Spam({self.n})'

l = [Spam(n) for n in range(5,0,-1)]
print(top(l,2))
