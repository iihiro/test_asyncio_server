# -*- coding: utf-8 -*-

import asyncio

async def test_server(reader, writer):
    
    cnt = 0
    
    while True:
        rmsg = await reader.readline()
        if rmsg == b'':
            break
        if rmsg:
            smsg = '[s] ack %d\n' % cnt
            writer.write(smsg.encode())
            await writer.drain()
            print('[s] send %s' % smsg)
            cnt += 1
    
    print('[s] connection closed')
    await writer.drain()
    writer.close()

    
def start(host, port):
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(test_server, host, port, loop=loop)
    serv = loop.run_until_complete(coro)

    print('[s] serving on {}'.format(serv.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    serv.close()
    loop.run_until_complete(serv.wait_closed())
    loop.close()

if __name__ == '__main__':
    start('127.0.0.1', 12345)
