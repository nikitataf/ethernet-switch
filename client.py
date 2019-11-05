"""Client.

The clients send a message to random destination NODE ADDRESSes in range 1..10 every second.
"""

__version__ = '0.1'
__author__ = 'Nikita Tafintsev'

import socket
import time
import random


start_time = time.time()
node_address = int(input('Insert node address: '))
numbers = list(range(1, 11))
numbers.remove(node_address)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9090))

while True:
    dst = random.choice(numbers)
    output_string = str(node_address) + ', ' + str(dst)
    print('NODE ' + str(node_address) + ' sends to NODE ' + str(dst))
    sock.send(output_string.encode())
    time.sleep(1)
    msg = sock.recv(1024)
    if msg:
        print("--- %s seconds ---" % (time.time() - start_time))
        print(msg.decode())
