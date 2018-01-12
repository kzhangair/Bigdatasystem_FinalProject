import socket
import threading
import random
import time

bind_ip = '0.0.0.0'
bind_port = 10001   # !!!CHANGE THIS!!!

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(100)  # max backlog of connections

print 'Listening on {}:{}'.format(bind_ip, bind_port)


def handle_client_connection(client_socket, stream_index):
    stream_index
    
    random.seed(time.time())

    offset = random.randint(0, 86400)   # initial time difference (less than 1 day)
    speed_level = random.randint(1, 4)   # stream speed level

    topic = 'topic ' + str(stream_index) + ' '
    
    while True:
        t = time.time() + offset
        x = random.randint(0, 2**20)    # int_val range [0,2^20]
        client_socket.send(topic + str(t) + " " + str(x) + "\n")
        time.sleep(max(0.01, random.randint(0, speed_level * 20) / 1000.0))    # 0.01 <= stream interval <= level * 0.02 (seconds)

    client_socket.close()

stream_index = 0

while True:
    client_sock, address = server.accept()
    print 'Accepted connection from {}:{}'.format(address[0], address[1])
    stream_index += 1
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock, stream_index)
    )
    client_handler.start()
