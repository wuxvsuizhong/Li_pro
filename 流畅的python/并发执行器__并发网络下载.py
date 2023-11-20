# 顺序下载
import time
from pathlib import Path
from typing import Callable
import httpx

POP20_CC = ('CH IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://mp.ituring.com.cn/files/flags'
DEST_DIR = Path('download')

def save_flag(img:bytes,filename:str)->None:
    (DEST_DIR/filename).write_bytes(img)

def get_flag(cc:str)->bytes:
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url,timeout=6.1,follow_redirects=True)
    resp.raise_for_status()
    return resp.content

def download_many_sequence(cc_list:list[str])->int:
    for cc in sorted(cc_list):
        image = get_flag(cc)
        save_flag(image,f'{cc}.gif')
        print(cc,end=' ',flush=True)
    return len(cc_list)

def main(downloader:Callable[[list[str]],int])->None:
    DEST_DIR.mkdir(exist_ok=True)
    t0=time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')


# if __name__ == "__main__":
#     main(download_many_sequence)

# ###################################
# 使用concurrent.futures模块下载——线程池
# ###################################
from concurrent import futures

def download_one(cc:str):
    image = get_flag(cc)
    save_flag(image,f'{cc}.gif')
    print(cc,end = ' ',flush=True)
    return cc

def download_many_thread_pool(cc_list:list[str]) ->int:
    # 实例化futures.ThreadPoolExecutor作为上下文管理器，executor.__exit__方法将调用executor.shutdown(wait=True),在所有线程都执行完毕前阻塞线程
    with futures.ThreadPoolExecutor() as executor:
        # futures.ThreadPoolExecutor维持着一个线程池，分配任务，手机结果的队列
        # ThreadExecutor默认有一个默认的参数max_workers = min(32,os.cou_count()+4)，限定有多少个线程
        # os.cou_count()至少是1，所以max_workers最小是5个线程
        res = executor.map(download_one,sorted(cc_list))
        # executor.map和通用map调用类似，不过插入的目标任务函数download_one会在多个线程中并发调用

    return len(list(res))

# if __name__ == "__main__":
#     main(download_many_thread_pool)

# ###############################
# 使用concurrent.futures.Futrue对象
# ###############################
def download_many_by_futrue(cc_list:list[str]) ->int:
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list):
            # 先循环使用submit创建并排定futrue对象
            future = executor.submit(download_one,cc)
            to_do.append(future)
            print(f'Schedule for {cc}: {future}')

        for count,future in enumerate(futures.as_completed(to_do),1):
            # 迭代使用as_complete获取Future的结果
            res: str = future.result()
            print(f'{future} result:{res!r}')

    return count

# if __name__ == "__main__":
#     main(download_many_by_futrue)
    # 输出
    # Schedule for BR: <Future at 0x23c84da5450 state=running>
    # Schedule for CH: <Future at 0x23c84c98410 state=running>
    # Schedule for ID: <Future at 0x23c84da4f10 state=running>
    # Schedule for IN: <Future at 0x23c84da5b10 state=pending>
    # Schedule for US: <Future at 0x23c84da6890 state=pending>
    # CH <Future at 0x23c84c98410 state=finished returned str> result:'CH'
    # BR <Future at 0x23c84da5450 state=finished returned str> result:'BR'
    # ID <Future at 0x23c84da4f10 state=finished returned str> result:'ID'
    # IN <Future at 0x23c84da5b10 state=finished returned str> result:'IN'
    # US <Future at 0x23c84da6890 state=finished returned str> result:'US'
    #
    # 5 downloads in 1.34s

    # 从输出可以看到，一开始的时候，只有3个Futrue处于running状态，其余的都处于pending状态，因为在download_many_by_futrue设置了入参max_workers = 3
    # 对于IO密集型任务，使用ThreadPoolExecutor，对于计算密集型任务，使用ProcessPoolExecutor

# ######################################
# 使用ProcessPoolExecutor——多核版素数检测程序
# ######################################
import sys
from concurrent import futures
from time import perf_counter
from typing import NamedTuple

from python并发模型__自建线程池 import is_prime,NUMBERS

class PrimeResult(NamedTuple):
    n:int
    flag:bool
    elapsed:float

def check(n:int)->PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n,res,perf_counter() - t0)

def main_get_prime() ->None:
    if len(sys.argv) < 2:
        workers = None
    else:
        workers = int(sys.argv[1])

    executor = futures.ProcessPoolExecutor(workers)
    actual_workers = executor._max_workers

    print(f'使用{actual_workers}个进程检查{len(NUMBERS)}个数字:')

    t0 = perf_counter()
    numbers = sorted(NUMBERS,reverse=True)
    with executor:
        for n,prime,elapsed in executor.map(check,numbers):
            label = 'P' if prime else ' '
            print(f'{n:16} {label} {elapsed:9.6f}s')
    time = perf_counter() - t0
    print(f'总共消耗时间:{time}')


# if __name__ == "__main__":
#     main_get_prime()
    # 使用8个进程检查20个数字:
    # 9999999999999999    0.000010s
    # 9999999999999917 P  7.697590s
    # 7777777777777777    0.000010s
    # 7777777777777753 P  6.926292s
    # ...
    # 观察输出结果，因为NUMBERS数据是顺序提交，第一个数很快获得结果。但是第二个数很久才有结果，并且后续的其他数据的结果也适合第二个数字的经过一并出现的
    # 因为第二个数字是NUMBERS列表中最大的素数，计算时间最长，当第二个数字检测完毕后，其他的数字已经完成了计算分析，只是计算结果等到第二个数字出来后才出来


# ##################
# 对executpr.map的研究
# ##################
from time import sleep,strftime
from concurrent import futures

def display(*args):
    """获取当前时间[时:分:秒]，在传入的msg字符串前添加这个格式的时间展示"""
    print(strftime('[%H:%M:%S]'),end=' ')
    print(*args)

def loiter(n):
    msg = '{}loiter({}): doing nothong for {}s...'
    display(msg.format('\t'*n,n,n))
    sleep(n)
    msg = '{}loiter({}):done'
    display(msg.format('\t'*n,n))
    return n*10

def main():
    display('Script starting。。。')
    executor = futures.ThreadPoolExecutor(max_workers=3)
    results = executor.map(loiter,range(5)) # executor.map的返回结果一个迭代器
    display('results:',results)
    display('Wating for invalid results:')
    for i,result in enumerate(results): # enumerate迭代results，隐式的调用results这个迭代器的__next__方法
        display(f'result: {i}: {result}')
        # 因为会隐式地调用results迭代器的__next__方法，而__next__方法会等待各个任务对昂的结果，所以中途如果有施行时间比较长的task，会再获取结果的时候阻塞、
        # 但是这里只是获取结果的这一动作的阻塞，其实各个task还是在并行的在执行的


if __name__ == "__main__":
    main()
    # [21:39:45] Script starting。。。
    # [21:39:45] loiter(0): doing nothong for 0s...
    # [21:39:45] loiter(0):done
    # [21:39:45] 	loiter(1): doing nothong for 1s...
    # [21:39:45] 		loiter(2): doing nothong for 2s...
    # [21:39:45] 			loiter(3): doing nothong for 3s...
    # [21:39:45] results: <generator object Executor.map.<locals>.result_iterator at 0x000001B40658B540>
    # [21:39:45] Wating for invalid results:
    # [21:39:45] result: 0: 0
    # [21:39:46] 	loiter(1):done
    # [21:39:46] 				loiter(4): doing nothong for 4s...[21:39:46] result: 1: 10
    #
    # [21:39:47] 		loiter(2):done
    # [21:39:47] result: 2: 20
    # [21:39:48] 			loiter(3):done
    # [21:39:48] result: 3: 30
    # [21:39:50] 				loiter(4):done
    # [21:39:50] result: 4: 40

    # 从中间的打印results: <generator object Executor.map.<locals>.result_iterator at 0x000001B40658B540>可是看出，results作为concurrent.ThreadPoolExecutor.map的返回结果，他是一个迭代器，
    # loiter函数按照传入的数据值n休眠，第一个传入0所有休眠0秒，随机立即done
    # 在第一个Thread结束后，因为设置的ThreadPoolExecutor设置的最大workers为3，所以同时启动了3个Thread,分别是loiter(1)，loiter(2)，loiter(3),然后因为超过了最大max_workers=3，loiter(4)只能等待
    # 当 loiter(1)结束后，有空余的线程，所以loiter(4)得以执行，之后没有新增加的任，所以各个thread相继done
    # 迭代executor.map获取结果，如果刚好遇到有结果未返回，那么得带获取结果的动作会在当前阻塞，但是实际的任务还是在并行执行的，所以最好是等到所有的task执行完毕后，在去迭代的获取结果

# ################
# 显示进度条并处理错误
# ################
from collections import Counter
from http import HTTPStatus
import httpx
import tqdm
from concurrent.futures import ThreadPoolExecutor,as_completed

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

def get_flag(base_url: str,cc:str)->bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url,timeout=3.1,follow_redirects=True)
    resp.raise_for_status()
    return resp.content

def download_one(cc:str,base_url:str,verbose:bool=False):
    try:
        image = get_flag(base_url,cc)
    except httpx.HTTPStatusError as exc:
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            msg = f'not found {res.url}'
        else:
            raise
    else:
        save_flag(image,f'{cc}.gif')
        msg = 'OK'

    if verbose:
        print(cc,msg)

    return

def download_many(cc_list:list[str],base_url:str,verbose:bool,_unused_concur_req:int):
    counter = Counter()
    cc_iter = sorted(cc_list)
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter)
    for cc in cc_iter:
        try:
            status = download_one(cc,base_url,verbose)
        except httpx.HTTPStatusError as exc:
            error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
            error_msg = error_msg.format(resp = exc.response)
        except httpx.RequestError as exc:
            error_msg = f'{exc} {type(exc)}'.strip()
        except KeyboardInterrupt:
            break
        else:
            error_msg = ''

        if error_msg:
            status = 'ERROR'
            counter[status] += 1
            if verbose and error_msg:
                print(f'{cc} error:{error_msg}')

    return counter

