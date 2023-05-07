#############
#向yield发送值
#############
def test_send():
  res = yield "hello"
  yield res

g1 = test_send()

print(next(g1))
# g1.send("world")   #不打印的话看不出效果，send是直接就发送值给了 res = yeild "hello" 前面的res了，所以test_send在接收到send的值后会直接向下走到yield res 直接返回而无需next
print(g1.send("world"))  #这里直接返回了，可以看到打印效果

############
#使用yield from
print("######遍历多个yield######")
def test_mul_yield():
  for s in 'abc':
    yield s
  for i in range(3):
    yield i


for i in test_mul_yield():
  print(i)
print("########使用生成器遍历多个yield#########")
g2 = test_mul_yield()
while True:
  try:
    print(next(g2))
  except StopIteration:
    break


print("########使用yield from#########")
def test_from():    # 使用yield from简化test_mul_yield函数的写法
  yield from 'abc'
  yield from range(3)

for i in test_from():
  print(i)
print("########使用生成器遍历yield from#########")
g3 = test_from()
while True:
  try:
    print(next(g3))
  except StopIteration:
    break

################
print("yield from作为连接调用者和自生成器之间的通道")
################
def sub():
  yield 'a'
  yield 'b'
  
  return 'c'

def link():
  res = yield from sub()  #前两次都是直接从此处的yield返回的，同时yiels from后面需要跟一个生成器或者可迭代对象
  print("结果",res)  #这里只会代用一次 ”结果” c

g = link()
while True:
  try:
    print(next(g))
  except StopIteration:
    break

