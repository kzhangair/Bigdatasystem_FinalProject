import socket
import threading

streaming1_server_name='localhost'
streaming1_port=10001
streaming2_server_name='localhost'
streaming2_port=10001

client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client1.connect((streaming1_server_name, streaming1_port))
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect((streaming2_server_name, streaming2_port))

fo = open('streamOutput', 'wb')

topic1Buffer = []
topic2Buffer = []

def resvTopic1():
    global topic1Buffer
    while(True):
        response1 = client1.recv(4096)
        resWords1 = response1.split(" ")
        time1 = float(resWords1[2])
        value1 = int(resWords1[3])
        topic1Buffer.append((time1, value1))

def resvTopic2():
    global topic2Buffer
    while(True):
        response2 = client2.recv(4096)
        resWords2 = response2.split(" ")
        time2 = float(resWords2[2])
        value2 = int(resWords2[3])
        topic2Buffer.append((time2, value2))
            
            
t1 = threading.Thread(
    target=resvTopic1
)
t1.start()
t2 = threading.Thread(
    target=resvTopic2
        )
t2.start()

index = 0
start = 0
while (True):
    if(len(topic1Buffer)<=5 or len(topic2Buffer)<=30):
        continue
    curT1 = topic1Buffer[index][0]
    curValue1 = topic1Buffer[index][1]
    L = curT1-30
    H = curT1+30
    while(start >= len(topic2Buffer)):
        continue
    curT2 = topic2Buffer[start][0]
    curValue2 = topic2Buffer[start][1]
    stop = start
    while curT2 >= L and curT2 <=H:
        if(curValue2 == curValue1):
            print "topic1: %f, %d\n" % (curT1, curValue1)
            print "topic2: %f, %d\n" % (curT2, curValue2)
            print 'topic 1 ' + str(curT1) + ' topic 2 ' + str(curT2) + ' ' + \
                 str(curValue1) + '\n'
            fo.write('topic 1 ' + str(curT1) + ' topic 2 ' + str(curT2) + ' ' + \
                 str(curValue1) + '\n')
            fo.flush()
        stop += 1
        while(stop >= len(topic2Buffer)):
            continue
        curT2 = topic2Buffer[stop][0]
        curValue2 = topic2Buffer[stop][1]
    if curT2 < L:
        start += 1
    elif curT2 > H:
        index += 1
fo.close()
print "Exit!"