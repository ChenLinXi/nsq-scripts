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

class Writer(threading.Thread):
    def __init__(self, t_name, queue, addr='nsq-ip' ,topic=""):
        threading.Thread.__init__(self,name=t_name)
        self.data = queue
        self.addr = addr
        self.topic = topic
        try:
            self.writer = nsq.Writer(nsqd_tcp_addresses=[self.addr])
        except Exception,e:
            print e
    
    def pub_message(self):
        try:
            self.writer.pub(self.topic, self.data.get(1), self.finish_pub) #callback
        except Exception,e:
            print e
    
    def finish_pub(self, conn, res):
        print 'Write:' + str(res)
        
    def run(self):
        tornado.ioloop.PeriodicCallback(self.pub_message, 500).start()
    
