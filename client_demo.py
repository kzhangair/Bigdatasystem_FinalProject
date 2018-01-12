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
    while(True):
        response1 = client1.recv(4096)
        resWords1 = response1.split(" ")
        curT1 = float(resWords1[2])
        curValue1 = int(resWords1[3])
        topic1Buffer.append((curT1, curValue1))

def resvTopic2():
    while(True):
        response2 = client2.recv(4096)
        resWords2 = response2.split(" ")
        curT2 = float(resWords2[2])
        curValue2 = int(resWords2[3])
        topic2Buffer.append((curT2, curValue2))

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
stop = 0
while (True):
    
    curT1 = topic1Buffer[index][0]
    curValue1 = topic1Buffer[index][1]
    L = curT1-30
    H = curT1+30
    
    while(stop - start > 0):
        if topic2Buffer[start][0] < L:
            start += 1
        else :
            break

    curT2 = topic2Buffer[stop][0]
    curValue2 = topic2Buffer[stop][1]

    for i in range(len(resBuffer)):
        if(resBuffer[i][1] == curValue1):
            print "%f, %d\n" % (curT1, curValue1)
            print "%f, %d\n" % (resBuffer[i][0], resBuffer[i][1])
            print 'topic 1 ' + str(curT1) + ' topic 2 ' + str(resBuffer[i][0]) + ' ' + \
                     str(curValue1) + '\n'
            fo.write('topic 1 ' + str(curT1) + ' topic 2 ' + str(resBuffer[i][0]) + ' ' + \
                     str(curValue1) + '\n')
fo.close()
print "Exit!"