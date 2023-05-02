from multiprocessing import Process
import time

def func(name):
    print(f"{name}开始")
    time.sleep(10)
    print(f'{name}结束')

# 在windows上，常见进程的时候会使用类似模块导入额方式，也就是import
# 这会导致一个问题，如果创建进程的代码不是放在 __main__函数下，每次导入的时候是会被执行一边的
# 于是在windows下，导入的子进程又会中Process创建进程，在新的子进程中又会执行Process创建进程，一直递归下去
# p = Process(target=func,args=('子进程工作...',))
# p.start()

# 要结局windows下递归创建进程的问题，只需要把Process创建进程的步骤放在 __main__函数里面就行
# 这要在windows上创建进程的时候，类似于import步骤的时候，就不会执行 __main__ 里面的代码，使得创建进程Process只执行一次
if "__main__" == __name__ :
    p = Process(target=func,args=("子进程工作...",))
    p.start()
    print("主进程...")