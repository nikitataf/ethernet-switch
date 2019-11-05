"""Replica of  Ethernet switch.

The switch operates on messages that include the source and destination NODE ADDRESS.
"""

__version__ = '0.1'
__author__ = 'Nikita Tafintsev'

import socket
from _thread import *
import copy
import time


def send(src, dst):
    """
    Switch decides where to forward the message:
    -If the switch knows how to reach a given destination, the message is sent there
    -If it does not know, the message is broadcast to all connected clients (just like a normal Ethernet switch)
    -The message is never sent to the connection from where it was received
    -If there are no connections to send the message it is discarded

    :param src: source NODE ADDRESS
    :param dst: destination NODE ADDRESS
    """
    if dst in list_of_all_devices:
        client_socket = list_of_all_devices[dst]
        msg = ' NODE '+str(dst)+' received from NODE '+str(src)
        client_socket.send(msg.encode())
    else:
        buff_dict = copy.copy(list_of_all_devices)
        del buff_dict[src]
        if not buff_dict:
            client_socket = list_of_all_devices[src]
            msg = 'Delivered to the switch, no other connected nodes'
            client_socket.send(msg.encode())
        else:
            print('Broadcast to all connected devices: ', list(buff_dict.keys()))
            for source, client_socket in buff_dict.items():
                msg = ' Message from node ' + str(src) + '. Destination ' + str(dst) + ' is unreachable. '
                client_socket.send(msg.encode())


def on_new_client(client_socket):
    """
    Function retrieves source and destination NODE ADDRESSes,
    it creates dictionary of all connected NODEs and send a message to a destination NODE
    :param client_socket: socket object
    """
    while True:
        msg = client_socket.recv(1024)
        if msg:
            msg_str = msg.decode()
            buff = str(msg_str).partition(', ')
            src = buff[0]
            dst = buff[2]
            print("--- %s seconds ---" % (time.time() - start_time))
            print('NODE ' + str(src) + ' --> NODE ' + str(dst))
            list_of_all_devices[src] = client_socket
            send(src, dst)
        else:
            break
    client_socket.close()
    list_of_all_devices.pop(src, None)


start_time = time.time()
list_of_all_devices = {}
s = socket.socket()
s.bind(('', 9090))
s.listen(100)  # put the socket into listening mode
print('Switch started!', 'Waiting for clients...')
while True:
    c, address = s.accept()  # establish connection with client
    print('Got connection from a new node')
    start_new_thread(on_new_client, (c,))  # create new thread
