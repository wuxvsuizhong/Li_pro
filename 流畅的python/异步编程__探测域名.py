import asyncio
import socket
from keyword import kwlist
from pathlib import Path

POP20_CC = ('CH IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://mp.ituring.com.cn/files/flags'
DEST_DIR = Path('download')
MAX_KEYWORD_LEN = 4

async def probe(domain:str)->tuple[str,bool]:
    loop = asyncio.get_running_loop()   # 启动事件循环
    try:
        await loop.getaddrinfo(domain,None)     # loop.getaddrinfo 协程方法，返回一个5元组
    except socket.gaierror:
        return (domain,False)
    return (domain,True)

async def main()->None:
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    domains = (f'{name}.dev'.lower() for name in names)
    coros = [probe(domain) for domain in domains]   # 构建一个协程对象列表
    for coro in asyncio.as_completed(coros):
        # print('-'*10)
        domain,found = await coro
        mark = '+' if found else ' ' # 根据协程对象probe的返回结果，判断
        print(f'{mark} {domain} ')
#
# if __name__ == "__main__":
#     asyncio.run(main())

# ##############
# 异步版本国旗下载器
# ##############
from httpx import AsyncClient
from typing import Callable
import time
def download_many(cc_list:list[str])->int:
    return asyncio.run(supervisor(cc_list))

async def  supervisor(cc_list:list[str])->int:
    async with AsyncClient() as client: # 启动事件循环
        to_do = [download_one(client,cc) for cc in cc_list] # 每一次的下载都会调用一次download_one协程，这里构建一个协程对象列表
        res = await asyncio.gather(*to_do)  #接受一个或者可异步调用对象，等待全部执行完毕，并按照可以不调用对象的提交顺序返回结果列表
    return len(res) # 返回结果列表长度

def save_flag(image:bytes,fname:str):
    (DEST_DIR/fname).write_bytes(image)

async def get_flag(client:AsyncClient,cc:str)->bytes:
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url,timeout=6.1,follow_redirects=True)
    return resp.read()

async def download_one(client: AsyncClient,cc: str):
    image = await get_flag(client,cc)
    save_flag(image,f'{cc}.gif')
    print(cc,end=' ',flush=True)
    return cc

def main(downloader:Callable[[list[str]],int])->None:
    DEST_DIR.mkdir(exist_ok=True)
    t0=time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')

if __name__ == "__main__":
    main(download_many)