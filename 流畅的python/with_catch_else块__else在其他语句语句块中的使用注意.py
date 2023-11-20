# else同for语句块对其时的使用

# else在
for i in range(10):
    print('-'*3,i,'-'*3,end=' ')
else:
    print("循环正常结束")
# 输出：
#     --- 0 --- --- 1 --- --- 2 --- --- 3 --- --- 4 --- --- 5 --- --- 6 --- --- 7 --- --- 8 --- --- 9 --- 循环正常结束

for i in range(10):
    if i == 5:
        break
    print('-'*3,i,'-'*3,end=' ')
else:
    print("循环正常结束")
print()

# 输出
# --- 0 --- --- 1 --- --- 2 --- --- 3 --- --- 4 ---

# 总结：当else和for语句对其使用时，只哟在fore语句正常结束循环，且没有经过break退出循环时，else语句快中的内容才会被执行到

# ######################
# else和while语句的对其使用
# ######################
cnt = 0
while cnt < 10:
    print('cnt:',cnt,end=' ')
    cnt+=1
else:
    print("while 循环正常完成")

# 输出
# cnt: 0 cnt: 1 cnt: 2 cnt: 3 cnt: 4 cnt: 5 cnt: 6 cnt: 7 cnt: 8 cnt: 9 while 循环正常完成
cnt = 0
while cnt < 10:
    print('cnt:',cnt,end=' ')
    if cnt + 1 > 6:
        break
    cnt += 1
else:
    print("while 循环正常完成")   # 一旦while循环中执行了break，那么else语句块中的内容不会被执行

print()

# 输出
# cnt: 0 cnt: 1 cnt: 2 cnt: 3 cnt: 4 cnt: 5 cnt: 6

# 总结：只有while循环正常结束，且不被break终止循环时，再回执行对其的else语句块中的内容

# ###################
# else 和 try 对其的使用
# ###################
try:
    print(5/2)
except Exception as e:
    print(e)
else:
    print('执行和try对齐的else语句块.')
finally:
    print("执行finally")

# 输出
# 2.5
# 执行和try对齐的else语句块.
# 执行finally

try:
    print(5/0)
except Exception as e:
    print(e)
else:
    print('执行和try对齐的else语句块.')
finally:
    print("执行finally")

# 输出
# division by zero
# 执行finally

# 没有执行else语句块中的内容
# 也就是如果在try中发生了异常被except 捕获到了，那么就不会执行else语句块

try:
    print(5/0)
except ZeroDivisionError:
    print("捕获到除0异常")
else:
    print('执行和try对齐的else语句块.')
finally:
    print("执行finally")
# 输出
# 捕获到除0异常
# 执行finally

# 总结：同上一个例子，只要except中有不会异常，那么else语句块就不会执行
# 和try对齐的else语句块被执行的要求是，try中不能发生任何异常，异常不被except捕获
# finally语句是始终都会执行的

# ###############################################
# finally是否始终都会被执行，即便是在finally之前return?
# ###############################################

def myfunc(a,b):
    print("running myfunc。。。")
    try:
        r = a/b
        return r
    except Exception as e:
        print(e)
        # return -1     # 如果发生异常时，except块中的内容会被执行机，这时except里的return才有效
    else:
        print('执行和try对齐的else语句块.')
        return -1   # 如果是try中语句正常执行，且在try中return了，那么else语句中的return语句不会执行
        # 只有在try中的语句无语长，但是try中没有return，而在else中return了，那么else中的return才有效
    finally:
        print("执行finally")

ret = myfunc(5,0)
print(ret)
# running myfunc。。。
# division by zero
# 执行finally
# None

ret = myfunc(5,2)
print(ret)
# running myfunc。。。
# 执行finally
# 2.5

# 总结：finally始终都会被执行，且总会在return前执行
# 如果try语句中没有异常，但是try中没有return，而把return语句放在了else中，那么执行else中的return
# 如果try中有return语句，且try语句正常执行了，那么try的return有效，而不会执行else中的return
# 如果是try中的语句异常了，且被except捕获到了异常，那么如果except中有return，就会被执行且返回值有效
