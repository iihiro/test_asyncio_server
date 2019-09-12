# -*- coding: utf-8 -*-

import asyncio

async def test_client(host, port, n):
    
    reader, writer = await asyncio.open_connection(host, port)

    for i in range(n):
        smsg = 'hello %d\n' % i
        print('[c] send %s' % smsg)
        writer.write(smsg.encode())

        rmsg = await reader.readline()
        print('[c] recv %s' % rmsg.decode())

    writer.close()
    

def start(host, port):
    n = 10
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_client(host, port, n))

if __name__ == '__main__':
    start('127.0.0.1', 12345)
