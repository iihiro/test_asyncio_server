# -*- coding: utf-8 -*-

import asyncio

async def test_client(host, port, n, interval_sec):
    
    reader, writer = await asyncio.open_connection(host, port)

    async def func(i):
        smsg = 'hello %d\n' % i
        print('[c] send %s' % smsg)
        writer.write(smsg.encode())

        rmsg = await reader.readline()
        print('[c] recv %s' % rmsg.decode())

    if n < 0:
        i = 0
        while True:
            await func(i)
            i += 1
            await asyncio.sleep(interval_sec)
    else:
        for i in range(n):
            await func(i)
            await asyncio.sleep(interval_sec)

    writer.close()
    

def start(host, port, n=-1, interval_sec=0):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_client(host, port, n, interval_sec))

if __name__ == '__main__':
    start('127.0.0.1', 12345)
