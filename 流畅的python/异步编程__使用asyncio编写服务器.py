import asyncio
import functools
from pathlib import Path
from unicodedata import name
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from charindex import InvertedIndex

# #################
# 一个FastAPI web服务
# #################

STATIC_PATH = Path(__file__).parent.absolute() / 'static'

app = FastAPI(
    title='Mojifinder Web',
    description='通过名称查找unicode字符'
)

class CharName(BaseModel):
    char: str
    name: str

def init(app):
    app.state.index = InvertedIndex()
    app.state.form = (STATIC_PATH / 'form.html').read_text()

init(app)

@app.get('/search',response_model=list[CharName])
async def search(q:str):
    chars = sorted(app.state.index.search(q))
    return ({'char':c,'name':name(c)} for c in chars)

@app.get('/',response_class=HTMLResponse,include_in_schema= False)
def form():
    return app.state.form

# ################
# 一个简单的TCP服务器
# ################
import functools
import sys
from asyncio.trsock import TransportSocket
from typing import cast
from charindex import format_results

CLRF = b'\r\n'
PROMPT = b'?>'
async def finder(index:InvertedIndex,reader:asyncio.StreamReader,writer:asyncio.StreamWriter)->None:
    client = writer.get_extra_info('peername')
    while True:
        writer.write(PROMPT)
        await writer.drain()
        data = await reader.readline()
        if not data:
            break
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            query = '\x00'
        print(f'Form {client}:{query!r}')
        if query:
            if ord(query[:1]) < 32:
                break
            results = await search(query,index,writer)
            print(f'    To {client}: {results} resultd')
    writer.close()
    await writer.wait_closed()
    print(f'Close {client}')

async def search(query:str,index:InvertedIndex,writer:asyncio.StreamWriter)->int:
    chars = index.search(query)
    lines = (line.encode() + CLRF for line in format_results(chars))
    writer.writelines(lines)
    await writer.drain()
    status_line = f'{"--" * 66} {len(chars)} found'
    writer.write(status_line.encode() + CLRF)
    await writer.drain()
    return len(chars)



async def supervisor(index:InvertedIndex,host:str,port:int)->None:
    server = await asyncio.start_server(functools.partial(finder,index),host,port)
    socket_list = cast(tuple[TransportSocket,...],server.sockets)
    addr = socket_list[0].getsockname()
    print(f'Server on {addr}, Hit CTRL + C STOP')
    await server.serve_forever() # 在这里控制权进入事件循环，保持不动
    # 事件循环期间，针对连接服务器的每一个客户端。启动一个finder协程实例，从而让这个简单的服务器可以并发处理多个客户端，这个过程一直持续，直到服务器抛出KeyBoardInterrupt或者被操作系统终止


def main(host:str='127.0.0.1',port_arg:str = '2323'):
    port = int(port_arg)
    print('Building index')
    index = InvertedIndex()
    try:
        asyncio.run(supervisor(index,host,port))    # 启动事件循环
    except KeyboardInterrupt:
        print(f'\nServer shut Down')

if __name__ == "__main__":
    main(*sys.argv[1:])
