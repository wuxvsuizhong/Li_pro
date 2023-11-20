# ##############
# 线程实现的旋转指针
# ##############

import itertools,time
from threading import Thread,Event

def spin(msg:str,done:Event):
    for char in itertools.cycle( r'\|/-'):  # itertools.cycle在入参字符串上循环迭代
        status = f'\r{char} {msg}'  # \r让光标回到行的开头
        print(status,end='',flush=True)
        if done.wait(.2):   # 只有当在别处有调用done.set()的时候，这里才会返回True,进入if分支，break跳出
            break
    blanks = ' '* len(status)
    print(f'\r{blanks}\r',end='')

def slow() ->int:
    time.sleep(5)
    return 42

def supervisor()->int:
    done = Event()
    spinner = Thread(target=spin,args=('thinking in thread！',done))
    print(f"spinner object:{spinner}")
    spinner.start()
    res = slow()    #主线程sleep
    done.set()  # Event时间调用set()使其在其他线程的done.wait()立即返回True
    spinner.join()  #主线程等待子线程完成
    return res


def main():
    res = supervisor()
    print(f'Answer:{res}')

if __name__ == "__main__":
    main()


# ################
# 使用进程实现旋转指针
# ################

from multiprocessing import Process,Event
from multiprocessing import synchronize

def spin(msg:str,done:synchronize.Event):   #注意这里使用的是进程的Event，不过用法和线程的差不多
    for char in itertools.cycle( r'\|/-'):
        status = f'\r{char} {msg}'
        print(status,end='',flush=True)
        if done.wait(.2):
            break
    blanks = ' '* len(status)
    # print(f'\r{blanks}\r',end='')
    print(f'\r',end='')



def supervisor()->int:
    done = Event()
    spinner = Process(target=spin,args=('thinking in Process!',done))
    print(f'spinner object:{spinner}')
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result

def main2():
    res = supervisor()
    print(f'Answer:{res}')

if __name__ == "__main__":
    main2()

