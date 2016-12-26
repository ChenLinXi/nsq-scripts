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

class Execute(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name = t_name)
        self.data = queue
    
    def reporthook(self, block_read, block_size, total_size):
                global writeQueue
                if not block_read:
                        res = "connection opened"
                        #writeQueue.put(res)
                        return
                if total_size<0:
                        print "read %d blocks (%dbytes)" %(block_read,block_read*block_size)
                        res = 'read ' + str(block_read) + ' blocks (' + str(block_read*block_size) + 'bytes)'
                        #writeQueue.put(res)
                else:
                        amount_read=block_read*block_size;
                        print 'Read %d blocks,or %d/%d' %(block_read,block_read*block_size,total_size)
                        res = 'Read ' + str(block_read) + ' blocks,or ' + str(block_read*block_size) + '*' + str(total_size)
                        #writeQueue.put(res)
                return
                
    def _download(self, RES):
                try:
                        des = RES['path']+'/'+RES['filename']
                        msg = urllib.urlretrieve(RES['source'], des, reporthook = self.reporthook)
                        #print msg
                except Exception, e:
                        print e
                sys.stdout.flush()
                return True
                
    def _exec(self, RES):
                path = 'cd '+ RES['path'] + ' && '+ RES['Command']
                #print path
                try:
                        global writeQueue
                        res = os.popen(path).readlines()
                        writeQueue.put(res)
                        print res
                except Exception,e:
                        return e    
                        
    def run(self):
                #print 'begin exec'
                time.sleep(1)
                while(1):
                        global writeQueue
                        tmp = self.data.get(1).body
                        try:
                                RES = json.loads(tmp)
                        except Exception,e:
                                print e
                        des = RES['path']+'/'+RES['filename']
                        if os.path.exists(RES['path']):
                                if os.path.exists(des):
                                        retcode = self._exec(RES)
                                        print 'exec',retcode
                                else:
                                        self._download(RES)
                                        retcode = self._exec(RES)
                                        #print 'download and exec',retcode
                        else:
                                os.makedirs(RES['path'])
    
