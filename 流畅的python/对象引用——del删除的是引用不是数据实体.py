import weakref

s1={1,2,3}
s2 = s1
def bye():
    print("...lile tears in the rain.")

ender = weakref.finalize(s1,bye)    #为s1注册垃圾回收时的回调函数
print(ender.alive)  #检测s1是否还存活
del s1      #del删除一次对象的引用，但是可能不会使得数据被垃圾回收，垃圾回收只有当数据的引用减小到0的时候才会触发(del可以较小数据的引用计数从而使得数据的引用计数为0，触发垃圾回收)
print(ender.alive)  # True 数据仍然存活
s2 = 'span'     #s1和s2指向同一个对象{1,2,3}，del s1后减小了一次对象5引用计数，但是此时数据的计数还不是0，仍然有s2指向它，
# 但是当s2指向了其他的数据的时候，数据的引用计数就变为0，会触发垃圾回收
print(ender.alive)  #False 数据被垃圾回收