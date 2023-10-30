from functools import singledispatch
from collections import abc
import fractions
import decimal,html,numbers

@singledispatch
def htmlize(obj: object)->str:
    '''处理参数类型是基本类型object的基函数'''
    content =html.escape(repr(obj))
    return f'<pre>{content}</pre>'

@htmlize.register
def _(text: str)->str:
    '''处理参数类型是字符串的函数'''
    content = html.escape(text).replace('\n','<br/>\n')
    return f'<p>{content}</p>'

@htmlize.register
def _(seq:abc.Sequence) -> str:     #abc.Sequence是一个抽象类
    '''处理参数类型是列表，元组等,派生自abc.Sequence的一些可迭代类型的函数'''
    inner = '<li>\n<li>'.join(htmlize(item) for item in seq)
    return'<ul>\n<li>'+inner + '</li>\n</ul>'

@htmlize.register
def _(n:numbers.Integral)->str:     # Intergral是数字类型的抽象基类
    '''处理参数是派生自numbers.Integral的数字类型的函数'''
    return f'<pre>{n} (0x{n:x})</pre>'

@htmlize.register
def _(n:bool)->str:
    '''处理参数类型是bool类型的函数'''
    return f'<pre>{n}</pre>'

@htmlize.register(fractions.Fraction)
def _(x)->str:
    '''处理类型是分数类型的函数'''
    frac = fractions.Fraction(x)
    return f'<pre>{frac.numerator}/{frac.denominator}</pre>'

@htmlize.register(decimal.Decimal)
@htmlize.register(float)
def _(x) ->str:
    '''处理数据类型是小数类型的函数'''
    frac = fractions.Fraction(x).limit_denominator()
    return f'<pre>{x} ({frac.numerator}/{frac.denominator})</pre>'  # 把decimal类型按照分数显示

print(htmlize({1,2,3}))   #没有注册针对集合的函数，所以会调用参数为object的兜底函数
print(htmlize(abs))     # 会调用参数为object 的函数
print(htmlize('Heimlich & Co.\n- a game'))  # 调用参数为字符串的函数
print(htmlize(42))  # 调用参数为数字Integral的函数
print(htmlize(['alpha',66,{3,2,1}]))    # 调用参数为abc.Sequence的处理函数，迭代到每一个元素时又会转而去调用字符串，数组，以及object类型的函数({3,2,1}没有对应的类型注册函数，所以会使用兜底的object类型的注册函数)
print(htmlize((11,22,33)))  # 调用abc.Seqence类型的注册函数
print(htmlize({'a':1,'b':2}))   # 没有针字段的注册函数，会调用兜底的object函数
print(htmlize(fractions.Fraction(2,3)))     #fractions.Fraction分数类型,按照分数显示，调用哪个分数类型的注册函数
print(htmlize(2/3))     #实际是浮点数类型，所以会调用浮点数类型的注册函数
print(htmlize(decimal.Decimal('0.02380935')))   #decimal小数（浮点数)类型，调用响应的注册函数
print(htmlize(True))    #调用类型为bool类型的注册函数

# 输出
# <pre>{1, 2, 3}</pre>
# <pre>&lt;built-in function abs&gt;</pre>
# <p>Heimlich &amp; Co.<br/>
# - a game</p>
# <pre>42 (0x2a)</pre>
# <ul>
# <li><p>alpha</p><li>
# <li><pre>66 (0x42)</pre><li>
# <li><pre>{1, 2, 3}</pre></li>
# </ul>
# <ul>
# <li><pre>11 (0xb)</pre><li>
# <li><pre>22 (0x16)</pre><li>
# <li><pre>33 (0x21)</pre></li>
# </ul>
# <pre>{&#x27;a&#x27;: 1, &#x27;b&#x27;: 2}</pre>
# <pre>2/3</pre>
# <pre>0.6666666666666666 (2/3)</pre>
# <pre>0.02380935 (22831/958909)</pre>
# <pre>True</pre>

# 总结:
# 给函数使用@singledispatch装饰器后，将会给函数注册各种入参类型对应的处理各个子函数；
# 相当于面向对象中的函数重载，针对不同的入参有不同的函数原型；
# 注册类型处理的子函数的建议是尽量注册某种类型的抽象基类的类型，这样使用范围会更广
# 无法满足所有的类型时，注册object类型的处理函数兜底；