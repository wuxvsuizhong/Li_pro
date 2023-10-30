# ########################################
# 定义带有重载的签名的sum函数——使用overload装饰器
# ########################################

import functools
import operator
from collections.abc import Iterator
from typing import overload,Union,TypeVar

T = TypeVar('T')
S = TypeVar('S')

@overload
def sum(it:Iterator[T]) ->Union[T,int]:...
@overload
def sum(it:Iterator[T],/,start:S) ->Union[T,S]: ...
def sum(it,/,start=0):
    return functools.reduce(operator.add,it,start)

# #############
# py重写mymax函数
# #############

MISSING = object()
EMPTY_MSG = 'mymax() arg is an empty sequence'

from collections.abc import Callable,Iterable
from typing import Protocol,Any,TypeVar,overload,Union

class SupportsLessThan(Protocol):
    def __lt__(self, other:Any) -> bool:...

# T = TypeVar('T')
LT = TypeVar('LT',bound=SupportsLessThan)
DT = TypeVar('DT')

MISSING = object()
EMPTY_MSG = 'mymax() arg is an empty sequence'
@overload
# 匹配的是传参为一个个的位置参数，参数的类型为实现了SupportsLessThan协议的类型LT，但是传参没有提供key和default
def mymax(__arg1:LT,__arg2:LT,*args:LT,key:None = ...) -> LT:...
@overload
# 匹配参数传递时，提供了key但是没有提供default的场景
def mymax(__arg1:T,__arg2:T,*args:T,key:Callable[[T],LT]) ->T:...
@overload
# 和第一种类似，匹配的是传参为一个个的位置参数(可迭代对象)，参数的类型为实现了SupportsLessThan协议的类型LT，但是传参没有提供key和default
def mymax(__iterable:Iterable[LT],*,key:None = ...) -> LT:...
@overload
# 和第二个类似，匹配传参的时候如餐为可迭代的对象，提供了key，但是传参没有体统default的场景
def mymax(__iterable:Iterable[T],*,key:Callable[[T],LT]) ->T:...
@overload
# 入参为可迭代的对象，可迭代对象中的成员实现了SupportsLessThan协议，传参提供了default，但是没有提供key的场景，
def mymax(__iterable:Iterable[LT],*,key:None = ...,default=DT)->Union[LT,DT]:...
@overload
# 如餐为可迭代的对象，提供了key和default
def mymax(__iterable:Iterable[T],*,key:Callable[[T],LT],defult:DT) ->Union[T,DT]:...

def mymax(first,*args,key=None,default=MISSING):
    if args:
        series = args
        candidate = first
    else:
        series = iter(first)
        try:
            candidate = next(series)
        except StopIteration:
            if default is not MISSING:
                return default
            raise ValueError(EMPTY_MSG) from None

    if key is None:
        for current in series:
            if candidate < current:
                candidate = current
    else:
        candidate_key = key(candidate)
        for current in series:
            current_key = key(current)
            if candidate_key < current_key:
                candidate = current
                candidate_key = current_key

    return candidate




print(mymax(1,2,3))     # 3
print(mymax(['Go','Python','Rust']))    # Rust
print(mymax(1,2,-3,key=abs))        # -3
print(mymax([1,2,-3],default=0))    # 2
print(mymax([],default=None))   # None
print(max([1,2,-3],key=abs,default=None))  # -3
print(max([],key=abs,default=None))     # None
