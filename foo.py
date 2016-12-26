import os,sys,json
import nsq
import tornado.ioloop
import time
import threading
import Queue
import subprocess
import urllib2,urllib
from multiprocessing import Process

global readQueue
global writeQueue
#block Queue
readQueue = Queue.Queue(0)
writeQueue = Queue.Queue(0)

#multi threads
def foo():
        global readQueue, writeQueue
        r = Reader('Reader.', readQueue)
        w = Writer('Writer.', writeQueue)
        e = Execute('Exec.', readQueue)
        try:
                r.start()
                w.start()
                e.start()
        except Exception,e:
                print 'thread start error',e

        try:
                nsq.run()
        except Exception,e:
                print 'nsq run error',e

        try:
                r.join()
                w.join()
                e.join()
        except Exception,e:
                print 'thread join error',e
