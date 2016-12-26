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

class Reader(threading.Thread):
    def __init__(self, t_name, queue, addr='xx', topic="", channel=""):
        threading.Thread.__init__(self.name=t_name)
        self.addr = addr
        self.topic = topic
        self.channel = channel
        self.buf = []
        self.reader = nsq.Reader(message_handler=self.writeQ, loopupd_http_address=[self.addr], loopupd_poll_interval=15
                                topic=self.topic, channel=self.channel, max_in_flight=15)
        self.data = queue
    
    def writeQ(self, message):
        global writeQueue
        try:
            self.data.put(message)
        except Exception,e:
            print e
        time.sleep(0.5)
        return True
    
    def run(self):
        return 0
