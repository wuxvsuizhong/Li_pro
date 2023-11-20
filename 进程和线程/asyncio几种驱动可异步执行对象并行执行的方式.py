import asyncio
import locale


async def fun1(n:int):
    for _ in range(n):
        print('fun1...')
        await asyncio.sleep(1)
    return fun1

async def fun2(n:int):
    for _ in range(n):
        print('fun2...')
        await asyncio.sleep(1)
    return fun2

async def start0():
    """直接循环的await等待各个可异步执行对象的结果,相当于串行"""
    funs = [fun1(5), fun2(6)]
    req_count = len(funs)
    semaphore = asyncio.Semaphore(req_count)

    for f in funs:
        async with semaphore:
            await f # 直接循环的等待await，结果是各个f穿行执行，没有发挥异步协程额并行执行效果

async def start1():
    """异步协程并行执行的方式1：asyncio.as_comppleted(list)可驱动list中的可异步执行对象并行的执行"""
    funs = [fun1(5), fun2(6)]
    req_count = len(funs)
    semaphore = asyncio.Semaphore(req_count)

    it = asyncio.as_completed(funs) # 使用as_completed可以并行驱动可异步执行对象运行
    for f  in it:
        async with semaphore:
            ret = await f   # 此时迭代as_completed的结果，就是并行交替执行的
            print(ret)

async def start2():
    """异步协程并行执行的方式2: await asyncio.gather(f1,f2,f3...)可驱动f1,f2,f3并行执行"""
    funs = [fun1(5), fun2(6)]
    await asyncio.gather(*funs)
    print('start2 finish...')

async def start3():
    """
    异步协程并行执行的方式3：
    1）先使用asyncio.create_task(func)把各个可异步执行对象创建为Task对象(create_task返回的就是Task对象)；
    2）把各个Task对象放入可迭代的对象中，比如列表list中；
    3) await asyncio.wait(list) 驱动list中的各个可异步执行对象并行的执行；
    """
    task_list = [asyncio.create_task(fun1(5)),asyncio.create_task(fun2(6))]
    await asyncio.wait(task_list)

async def start4():
    """异步协程并行执行的方式4：还是先asyncio.create_task(func)把可异步执行对象func创建为Task，然后直接在后续串行await"""
    task1 = asyncio.create_task(fun1(5))
    task2 = asyncio.create_task(fun2(6))

    await task1
    await task2
    # await获取task的结果

    print('start4 finished。。。' )
    # 按照在start0()中的做法，这里的await为什么没有串行等待。因为在asyncio.create_task(func)的时候，在创建完Task对象的时候，已经把可异步执行对象加入到事件循环里面了，这里的await task只是在等待各个task的结果

async def fun_sametime(n):
    for _ in range(n):
        print('fun_sematime...')
        # await是阻塞等待后面跟的异步执行对象的结果
        # 从上到下的添加await，和串行执行没区别，失去了可异步调用的对象可并行执行的优势
        await asyncio.sleep(1)
        await fun1(1)



def main():
    # funs = [fun1(5), fun2(6)]
    # asyncio.run(funs) ERROR asyncio.run(func)，传入的func需要时async def定义的可异步执行对象才行

    # asyncio.run(start0())
    # asyncio.run(start1())
    # asyncio.run(fun_sametime(5))
    # asyncio.run(start2())

    # asyncio.run(start3())
    asyncio.run(start4())




if __name__ == "__main__":
    main()

# 总结：await关键字用于在异步对象中发起或者是等待另一个异步的协程对象执行完毕获取其结果，获取其结果，他是阻塞等待的
# 如果在一个异步协程对象(函数)中，串行添加await的动作，去分别等待各个异步执行对象的执行结果，那么整体各个添加的执行对象是串行执行的，在某种程度上来说，相当于是放弃了并行异步的功能
# 如果是要各个异步执行对象能够同时并行的执行，
# 方法1：可以把各个异步可执行对象（函数)放在可迭代列表list中，然后使用asyncio.as_completed(list)，as_completed这个方法返回一个可迭代对象，里面包含那些有执行进度，或者是已经有执行结果的异步对象的结果,他可以把传入的list中的可异步执行对象，驱动其并行执行
# 方法2:先把一个个的可异步执行对象添加到list中，然后await asyncio.gather(*list)，这样list中的可异步执行对象就是并行执行的
# 方式3：使用asyncio.create_task(func) 把可异步执行对象func创建为Task对象，然后再把创建好的各个Task对象添加到可迭代列表list中，最后使用await asyncio.wait(list),可驱动list中的各个可异步执行对象并行执行；