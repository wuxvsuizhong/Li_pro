from geolib import geohash as gh # type: ignore

# tuple参数注解
PRECISON = 9
def geohash(lat_lon:tuple[float,float]) -> str:   # 注解lat_lon参数，值为一个tuple,包含两个float字段
    return gh.encode(*lat_lon,PRECISON)

shanghai = 31.2304,121.4373
print(geohash(shanghai))   #wtw3em7fq
shanghai = 31,121
print(geohash(shanghai))    #wtw037ms0

# 在import的注解 type: ignore 会禁止mypy报告geolib没有类型提示
# 两次传递的shanghai坐标值不同，hash得到的结果也不同，虽然第二次传递的tuole里的值是int类型，但是运行不报错，说明类型注解只是个说明，不强制要求参数必须符合类型

# 使用NameTple具名元组作为类型注解，限定参数类型
from typing import NamedTuple
class Coordinate(NamedTuple):
    lat: float
    lon: float

def geohash(lat_lon: Coordinate) ->str:
    return gh.encode(*lat_lon,PRECISON)

def display(lat_lon:tuple[float,float]) -> str:
    lat,lon = lat_lon
    ns = 'N' if lat >= 0 else 'S'
    ew = 'E' if lon >= 0 else 'W'
    return f'{abs(lat):0.1f}° {ns},{abs(lon):0.1f}° {ew}'


print(geohash(Coordinate(31.2304,121.4373)))
# print(geohash(31.2304,121.4373))  #error geohash接受的是Coordinate类型
print(display(Coordinate(31.2304,121.437)))   # 格式化显示坐标

#################
# 注解不可变参数元组
################
from collections.abc import Sequence
# 注解返回值的类型是一个list,该list的元素类型是元组tuple，而这些一个个的tuple类型的元组中的元素为str,长度不定
# 如果想要注解长度不定，用作不了变列表的元组，则只能指定一个类型，后跟逗号和...,形如tuple[str,...]
# 如tupls[int,...]表示项为int的元组，省略号表示元素的数量>=1
# 长度不定的元组不能为字段执行不同的类型，也就是只能指定一种类型
# 类型可以用any,表示任意类型，如注解变量stuff:tuple[Any,...]也可写为 stuff:tuple表示stuff变量长度不定且元素类型任意
def columnsize(sequence:Sequence[str],num_columns: int = 0) -> list[tuple[str,...]]:
    if num_columns == 0:
        num_columns = round(len(sequence) ** 0.5)   # seqence列表的长度值开平方
    num_rows,reminder = divmod(len(sequence),num_columns)   # 用seqence的平方根，对sequnce的长度取商和取余数，商值为row_nums
    num_rows += bool(reminder) # 如果余数不为0，那么num_rows加1，num_rows就是分割seqencec的步长
    return [tuple(sequence[i::num_rows]) for i in range(num_rows)] # 一共num_rows组数据，从seqnece中分组取，步长为num_rows

anumals = 'drake fawn heron ibex koala lynx tahr xerus yak zapus'.split()
table = columnsize(anumals)
print(table)
for row in table:
    print(''.join(f'{word:10}' for word in row))