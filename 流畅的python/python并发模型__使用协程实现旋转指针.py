# ################
# 使用协程实现旋转指针
# ################
import asyncio
import itertools
import time


# 关键字async 定义的函数，就是一个协程对象
async def spin(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char}{msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.2)
        except asyncio.CancelledError:  # 捕获CanceledError，终止协程
            break
        blanks = ' ' * len(status)
        print(f'\r{blanks}\r', end='')


async def slow() -> int:
    await asyncio.sleep(10)
    # time.sleep(10)
    return 42

# spin和slow是两个协程对象

def main()->None:   # main是入口，是常规函数，其他函数都是协程函数
    print('-'*20,"使用协程实现旋转指针",'-'*20)
    result = asyncio.run(supervisor())  # 1.asyncio.run需要在常规函数中调用，同时是作为程序所有的协程代码的入口，他的作用就是启动时间循环，驱动协程运行，这里supervisor()就是一个协程对象
    # rayncio.run(func()) 这个调用将保持阻塞，一致等待func()的主体返回，
    print(f'Answer is:{result}')

# supervisor也是一个协程对象
async def supervisor()->int:
    spinner = asyncio.create_task(spin('thinnkomg！'))
    # asyncio.create_task 在协程函数中调用，调度另一个协程运行。
    # asyncio.create_task(func())调用不阻塞当前的协程的运行，而整个语句返回的是一个Task实例
    # Task实例中，包装着协程对象，提供控制和查询协程状态的方法

    print(f'spinner object:{spinner}')  # spinner object:<Task pending name='Task-2' coro=<spin() running at D:\script\code\python\Li_pro\流畅的python\python并发模型__使用协程实现旋转指针.py:9>>
    # 通过这里的打印可以看出spinner是一个%Task对象

    result = await slow()
    # await func() 在协程中调用，会把协程的控制权交给func()返回的协程对象，然后等待func()协程对象的返回值
    spinner.cancel()
    # 通过调用Task对象的cancel()方法，来抛出asyncio.CanceledError,让其在Task包装的协程对象中被捕获，从而终止协程
    return result

# 有一点值的注意的是，不论实在asyncio.run(func),还是在asyncio.create_task(func),或者在await func()中，
# func()的调用是立即返回一个写成对象，但是并不运行协程对象的函数主题，协程的主题的运行由事件循环驱动。

if __name__ == "__main__":
    main()

# 对比在slow中，把asyncio.sleep换成time.sleep的区别，前者能够维持旋转指针的打印，但是后者不行，后者会导致整个程序的线程阻塞(因为python只有一个执行流，除非是在启动额外的线程或者进程)

