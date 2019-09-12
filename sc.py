# -*- coding: utf-8 -*-

import time
import multiprocessing
import c

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
    test2()
