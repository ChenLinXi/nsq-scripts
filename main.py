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

#daemon process
def main():
    p = Process(target=foo)
    #p.daemon = True
    p.start()
    p.join()
        
if __name__ == '__main__':
    main()
