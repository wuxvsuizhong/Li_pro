import socket
import asyncio

server = socket.socket()
server.bind(("127.0.0.1",6000))
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.setblocking(False)
server.listen(10)

async def Accept(server):
    conn,addr = server.accept()
    return conn

async def toaccept(server):
    while True:
        try:
            conn = await asyncio.create_task(Accept(server))
            asyncio.create_task(read(conn))
        except BlockingIOError:
            pass


async def read(conn):
    while True:
        try:
            data = await conn.recv(1024)
            if not data:
                print("close1")
                conn.close()
                return
            else:
                conn.send(data.upper())
                return
        except BlockingIOError:
            pass
        except ConnectionResetError:
            print("close2")
            conn.close()
            return

asyncio.run(toaccept(server))

