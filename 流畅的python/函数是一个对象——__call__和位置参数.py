# python中，类只要实现了__call__方法，就可以表现的象函数一样
import random
class BingoCage:
    def __init__(self,items):
        self._items = list(items)
        random.shuffle(self._items)  #打乱items中的元素的顺序

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            # 如果self.items为空了，就抛出异常
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        return self.pick()

bingo = BingoCage(range(3))
print(bingo.pick())
print(bingo()) #有了__call__方法后，类可以表现的象函数一样使用()调用，并返回数据，这里bingo()其实调用的就是类BingoCage的__call__方法
print(callable(bingo)) #True 检验得出bingo是可调用的

##########################
# 位置参数和关键字参数的使用 #
#########################
# 一个生成html标签的例子
def tag(name,*content,class_=None,**attrs):
    # name/content是位置参数,class和attrs是关键字参数，
    # 关键字参数传递是形式如key=value的会被保存在attrs字典中
    """生成一个或者多个html标签"""
    if class_ is not None:
        attrs['class'] = class_ #把class也作为一个key放入attrs字典中，并赋值为传递的class_参数的值
    attr_pairs = (f' {attr} = "{value}"' for attr,value in sorted(attrs.items()))   #attrs就是标签的所有属性key=value的集合
    attr_str = ''.join(attr_pairs)
    if content:
        # attr_str是组成html标签中的，属性部分，name为标签名，c就是html标签的内容
        elements = (f'<{name}{attr_str}>{c}</{name}>' for c in content)
        return '\n'.join(elements)
    else:
        return f'<{name}{attr_str}/>'


print(tag('br'))    #<br/>   只传递了标签名name
print(tag('p','hello')) #<p>hello</p>   传递了标签名name和标签内容*content
print(tag('p','hello','world')) #<p>hello</p> <p>world</p>  传递了标签名和多个标签内容，则生成多个标签
print(tag('p','hello',id=3))    #<p id = "3">hello</p>  传递了标签名和内容，并传递了key=value这种标签的属性键值对
print(tag('p','hello','world',class_='slider')) #<p class = "slider">hello</p> <p class = "slider">world</p>    两个content内容，所以生成两个标签，每个标签有class=slider的属性
print(tag(content='testing',name='img')) #<img content = "testing"/>    一个img标签，并且通过kay=value形式的传参自定义指定html标签的属性

my_tag={'name':'img','title':"Sunset Boulevard","src":"sunset.jpg",'class':"framed"}
# 通过关键字拆包，传递参数到tag函数中
print(tag(**my_tag))    #<img class = "framed" src = "sunset.jpg" title = "Sunset Boulevard"/>

# 这里通过函数的位置参数，以及传递关键字参数，在tag函数中自动识别传递进来的参数是标签的name，还是标签的属性，还是标签的内容。还是是否是自封闭标签

###############################################
# 限定函数不要使用位数量不定的位置参数，而只使用关键字 #
##############################################      ·
def f(a,*,b):
    return a,b

print(f(1,b=2))
# print(f(1,2)) #error 在函数的定义形参中，使用了*，则*后面的参数就必须是按照关键字参数传递，也就是必须有b=val这种形式
                # *的位置也限定了最多能够传递多少个位置参数，在这里*前面只有一个参数a，所以想定了函数只能传一个位置参数
# print(f(1,2,b=3))   #error 只能传递一个位置参数，但是1，2都是位置参数，所以报错

######################
# 限定函数只使用位置参数 #
######################
# '/'出现在函数的形参定义上，它左边的是仅限位置参数，在'/'有右边的=可以指定其他参数
def divmod(a,b,/):  # 注意在py3.7版本之前不支持/语法

    return (a//b,a%b)

print(divmod(9,2))

#使用/重新定义tag函数
def tag(name,/,*content,calss_ = None,**attrs):
    pass
