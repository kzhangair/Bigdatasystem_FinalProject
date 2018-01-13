# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 17:04:12 2018

@author: Jahangair
"""

import socket
import time

streaming1_server_name='localhost'
streaming1_port=10001
streaming2_server_name='localhost'
streaming2_port=10001


client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client1.connect((streaming1_server_name, streaming1_port))
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect((streaming2_server_name, streaming2_port))

for i in range(6):
    print "%d hour" % (i+1)
    start = time.time()
    curTime = time.time()
    fo1 = open("topic1_batch"+str(i+1), 'wb')
    fo2 = open("topic2_batch"+str(i+1), 'wb')
    while(curTime - start < 3600):
        response1 = client1.recv(4096)
        fo1.write(response1)
        fo1.flush()
        response2 = client2.recv(4096)
        fo2.write(response2)
        fo2.flush()
        curTime = time.time()
client1.close()
client2.close()
fo1.close()
fo2.close()
    ## Add your processing codes here...

