# -*- coding: utf-8 -*-

import time
import multiprocessing
import c

def test3_3(host='127.0.0.1', port=12345):
    import s3
    disp = s3.Dispatcher()
    disp.start_daemon(host, port)

    async def putdata():
        for i in range(5):
            await asyncio.sleep(1)
            disp.put('putdata#%d' % i)
    
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        putdata(),
        c.test_client(host, port, 10, 0.5)))
    

def test3_2(host='127.0.0.1', port=12345):
    import s3
    disp = s3.Dispatcher()
    disp.start_daemon(host, port)

    c.start(host, port, n=10, interval_sec=0.5)

def test3_1(host='127.0.0.1', port=12345):
    import s3
    s3.start_daemon(host, port)

    c.start(host, port)

def test2(host='127.0.0.1', port=12345):
    import s2
    s2.start_daemon(host, port)

    c.start(host, port)

def test1(host='127.0.0.1', port=12345):
    import s
    sp = multiprocessing.Process(target=s.start, args=(host, port))
    sp.daemon = True
    sp.start()
    time.sleep(0.2)

    c.start(host, port)

if __name__ == '__main__':
    #test1()
    #test2()
    #test3_1()
    #test3_2()
    test3_3()
