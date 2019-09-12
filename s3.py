# -*- coding: utf-8 -*-

import time
import asyncio
import multiprocessing
from abc import ABCMeta, abstractmethod

class AbstractServer(metaclass=ABCMeta):

    def __init__(self, host, port):
        self._host = host
        self._port = port

    def start(self):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self._handle,
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

    @abstractmethod
    async def _handle(self, reader, writer):
        raise NotImplementedError()
     

class Server(AbstractServer):

    def __init__(self, host, port, in_queue=None, out_queue=None):
        super().__init__(host, port)
        self._in_queue = in_queue
        self._out_queue = out_queue

    async def _handle(self, reader, writer):
    
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
            external = self._in_queue.get() if not self._in_queue.empty() else 'none'
            print('[s] external %s' % external)
    
        print('[s] connection closed')
        await writer.drain()
        writer.close()

class Dispatcher(object):

    def __init__(self):
        self.__in_queue = multiprocessing.Queue()
        self.__out_queue = multiprocessing.Queue()
    
    def start_daemon(self, host, port):
        sp = multiprocessing.Process(target=self._start,
                                     args=(host, port,
                                           self.__in_queue,
                                           self.__out_queue))
        sp.daemon = True
        sp.start()
        time.sleep(0.2)

    def put(self, data):
        self.__in_queue.put(data)

    def get(self):
        return self.__out_queue.get()
        
    def _start(self, host, port, in_queue, out_queue):
        s = Server(host, port, in_queue, out_queue)
        s.start()
        
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

