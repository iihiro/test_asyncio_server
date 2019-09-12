# -*- coding: utf-8 -*-

import time
import asyncio
import multiprocessing

class Server(object):

    def __init__(self, host, port):
        self._host = host
        self._port = port

    def start(self):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.test_server,
                                    self._host, self._port, loop=loop)
        serv = loop.run_until_complete(coro)

        print('[s] serving on {}'.format(serv.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        serv.close()
        loop.run_until_complete(serv.wait_closed())
        loop.close()

    async def test_server(self, reader, writer):
    
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

def start_daemon(host, port):
    sp = multiprocessing.Process(target=start, args=(host, port))
    sp.daemon = True
    sp.start()
    time.sleep(0.2)
        
def start(host, port):
    s = Server(host, port)
    s.start()

if __name__ == '__main__':
    start('127.0.0.1', 12345)

