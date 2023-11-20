import asyncio
from collections import Counter
from http import HTTPStatus
from pathlib import Path
import httpx
import tqdm
import time
from typing import Callable

DEFAULT_COUNT_REQ = 5
MAX_CONCUR_REQ = 1000

async def get_flag(client:httpx.AsyncClient,base_url:str,cc:str)->bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url,timeout=3.1,follow_redirects=True)  # await的作用，等待它跟随的协程对象返回结果，如果协程中有耗时的操作，那么会交出资源，控制权交还给事件循环去运行其他的协程
    resp.raise_for_status()
    return resp.content

def save_flag(image:bytes,fname:str):
    (DEST_DIR/fname).write_bytes(image)

async def get_country(client:httpx.AsyncClient,base_url:str,cc:str)->str:
    """获取国家名称"""
    url = f'{base_url}/{cc}/metadata.json'.lower()
    resp = await client.get(url,timeout=3.1,follow_redirects=True)
    resp.raise_for_status()
    metadata = resp.json()
    return metadata['country']

async def download_one(client:AssertionError,cc:str,base_url:str,semaphore:asyncio.Semaphore,verbose:bool):
    try:
        async with semaphore:   # asyncio.semaphore的上下文，能够自动给信号量增/减（准确的说是在__aenter__进入时候递增信号量，在__aexit__时，递减信号量)
            image = await get_flag(client,base_url,cc)
        async with semaphore:   # 这里发起两个异步协程，但是这里是串行等待的
            country = await get_country(client,base_url,cc)
    except httpx.HTTPStatusError as exc:
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = "NOT FOUND"
            msg = f'{res.url} NOT FOUND'
        else:
            raise
    else:
        filename = country.replace(' ','_') # 获取国家名字
        # 异步保存文件的方式1：把任务通过to_thread委托给asyncio的线程池
        # 因为save_flag这个操作不是异步的，把save_flag这个io操作放在asyncio的线程池中去操作
        # await asyncio.to_thread(save_flag,image,f'{filename}.gif')  # 按照国家名字存储文件

        # 异步保存文件的方式2：把任务委托给执行机(默认的执行器是ThreadPoolExecutor)
        loop = asyncio.get_running_loop()   # 获取事件循环
        loop.run_in_executor(None,save_flag,image,f'{filename}.gif')

        status = 'OK'
        msg = 'OK'
    if verbose and msg:
        print(cc,msg)
    return status


async def supervisor(cc_list:list[str],base_url:str,verbose:bool,concur_req:int):
    counter = Counter()
    # 实例化信号量对象，限定最多只能有concur_req个线程使用该信号量
    semaphore = asyncio.Semaphore(concur_req)
    async with httpx.AsyncClient() as client:
        # 创建协程对象列表to_do,而download_one就是一个个的协程对象
        to_do = [download_one(client,cc,base_url,semaphore,verbose) for cc in sorted(cc_list)]
        to_do_iter = asyncio.as_completed(to_do)    # as_completed只返回已完成的协程对象结果
        if not verbose:
            # 进度条显示
            to_do_iter = tqdm.tqdm(to_do_iter,total=len(cc_list))
        error:httpx.HTTPError|None = None
        for coro in to_do_iter: #迭代已完成的协程对象结果
            try:
                status = await coro
                # 虽然await的原理是会等待coro返回结果，但是这里不会阻塞，因为这里的coro都是已经经过as_completed获取了的
                # 所以await会立即获得coro的结果，不会阻塞
            except httpx.HTTPStatusError as exc:
                error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
                error_msg = error_msg.format(resp = exc.response)
                error = exc
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
                error = exc
            except KeyboardInterrupt:
                break

            if error:
                status = 'ERROR'
                if verbose:
                    url = str(error.request.url)
                    cc = Path(url).stem.upper()
                    print(f'{cc} error: {error_msg}')
            counter[status] += 1
    return counter



def download_many(cc_list:list[str],base_url:str,verbose:bool,concur_req:int):
    coro = supervisor(cc_list,base_url,verbose,concur_req)  # supervisor创建协程对象coro
    counts = asyncio.run(coro)  # 协程对象由supervisor创建，在这里传递给asyncio.run,在run创建了事件循环之后，驱动协程对象coro去运行

    return counts

DEST_DIR = Path('download')
POP20_CC = ('CH IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://mp.ituring.com.cn/files/flags'

def main(downloader:Callable[[list[str]],int],default_count_req:int,MAX_CONCUR_REQ:int)->None:
    DEST_DIR.mkdir(exist_ok=True)
    t0=time.perf_counter()
    count = downloader(POP20_CC,BASE_URL,False,default_count_req)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')

if __name__ == "__main__":
    main(download_many,DEFAULT_COUNT_REQ,MAX_CONCUR_REQ)

