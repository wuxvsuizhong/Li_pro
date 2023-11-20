# 实现一个异步生成器
import asyncio
import os
import pathlib
import socket
import sys
from keyword import kwlist
from collections.abc import Iterable,AsyncIterable
from typing import NamedTuple,Optional
from pathlib import Path
class Result(NamedTuple):
    domain: str
    found: bool

OptionalLoop = Optional[asyncio.AbstractEventLoop]
async def probe(domain:str,loop:OptionalLoop = None)->Result:
    if loop is None:
        loop = asyncio.get_event_loop()
    try:
        await loop.getaddrinfo(domain,None)
    except socket.gaierror:
        return Result(domain,False)
    return Result(domain,True)

async def multi_probe(domains:Iterable[str])->AsyncIterable[Result]:
    loop = asyncio.get_running_loop()
    coros = [probe(domain,loop) for domain in domains]
    for coro in asyncio.as_completed(coros):
        result = await coro
        yield result    # 有了这一步,multi_probe就是一个异步生成器


async def main(tld:str)->None:
    tld = tld.strip('.')
    names = (kw for kw in kwlist if len(kw) <= 4)
    domains = (f'{name}.{tld}'.lower() for name in names)
    print('FOUND\t\tNOT FOUND')
    print('=====\t\t=====')
    async for domain,found in multi_probe(domains):
        # multi_probe 返回的是一个异步生成器，在这里使用async for来迭代获取其结果
        indent = '' if found else '\t\t'
        print(f'{indent}{domain}')

if __name__ == "__main__":
    # if len(sys.argv) == 2:
    #     asyncio.run(main(sys.argv[2]))
    # else:
    #     print('Please provide a TLD.',f'Exam0ple: {sys.argv[0]} COM.BR')
    asyncio.run(main('org'))

# 总结：在async def func(): 的函数体中，如果使用yield 那么。func就是一个异步生成器
# 如果不带有yield，那么func就是一个原生的协程，原生的协程可以返回None之外的任何值，但是异步生成器只能使用空的return 语句

# #####################
# 异步生成器用作上下文管理器
# #####################
from contextlib import asynccontextmanager
# 使用asynccontextmanager装饰器装饰的函数，在首次yield出现的位置之前的部分视为异步上下文管理器的__aenter__部分，在最后一次yield出现的后续部分的代码，视为__aeixt__部分

@asynccontextmanager
async def read_file_names(dir):
    """使用asynccontextmanager装饰器装饰的函数，可以创建为一个上下文管理器，后续使用async with在async def的函数中使用"""
    loop = asyncio.get_running_loop()   # 获取事件循环
    data = await loop.run_in_executor(None,os.listdir,Path(dir))    #把异步的功能函数转移到异步执行器中执行
    yield data # 返回数据，注意这里的yield是必须的

    print('over...')

async def start0():
    async with read_file_names('.') as data:
        print(data)


if __name__ == "__main__":
    asyncio.run(start0())
#     ['.mypy_cache', '.pytest_cache', 'charindex.py', 'dict处理缺失的值.py', 'download', ...]
# over...
# 这里先打印的是start0中的data的值,然后打印的是read_file_names中的over,也就是说先拿到read_file_names中yield返出来的值，然后再是执行read_file_names中yield后面的内容

# ##################
# 异步生成器和异步推导式
# ##################
async def start1():
    print('-' * 20, '异步生成器', '-' * 20)
    names = 'python.org rust-lang.org golang.org no-lang.invalid'.split()
    gen_found = (name async for name, found in multi_probe(names) if found)
    print(type(gen_found))  # <class 'async_generator'> 异步生成器类型
    async for name in gen_found:
        print(name)

async def start2():
    print('-' * 20, '异步推导式', '-' * 20)
    names = 'python.org rust-lang.org golang.org no-lang.invalid'.split()

    coros = [probe(name) for name in names]
    print(await asyncio.gather(*coros))
    # 异步推导式的结果是一个个的Result对象组成的列表
    # [Result(domain='python.org', found=True), Result(domain='rust-lang.org', found=True), Result(domain='golang.org', found=True), Result(domain='no-lang.invalid', found=False)]

    # 或者是
    print([await probe(name) for name in names])
    # [Result(domain='python.org', found=True), Result(domain='rust-lang.org', found=True), Result(domain='golang.org', found=True), Result(domain='no-lang.invalid', found=False)]

    # 可以在推导式中使用async for和await
    a1 = {name:found async for name,found in multi_probe(names)}
    a2 = {name for name in names if (await probe(name)).found}

    print(a1)   # {'python.org': True, 'golang.org': True, 'rust-lang.org': True, 'no-lang.invalid': False}
    print(a2)   #{'python.org', 'rust-lang.org', 'golang.org'}




if __name__ == "__main__":
    # asyncio.run(start1())
    asyncio.run(start2())



