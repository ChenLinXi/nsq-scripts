import os
import sys
import time
import subprocess
import json
import random

while(1):
	time.sleep(2)
	ID = random.randint(0,999999)
	msg = {"ID":ID,"Command":"python xxx.py","IsExit":"Y","source":"http://ip/xxx.py","filename":"xxx.py","path":"/root/monitor/scripts"}
	ip = 'http://nsq-tcp-ip/put?topic=topicName'
	json_msg = json.dumps(msg).encode('utf-8')
	#print json_msg, ip
	res = 'curl -d ' + '\''+ json_msg + '\'' +  ' '+ '\''+ ip + '\''
	#print res
	res = subprocess.Popen(res ,shell=True)
