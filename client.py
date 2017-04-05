#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import psutil
import socket

from json import dumps
from sys import argv
from time import sleep


INTERVAL_IN_SEC = 10

if len(argv) != 3:
    raise ValueError("Nieprawidłowa liczba argumentów: (host, port)")


host, port = argv[1], int(argv[2])


try:
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        memory_used_percent = psutil.virtual_memory().percent
        cpu_used_percent = psutil.cpu_percent(interval=1)
        data = {'memory_used_percent': memory_used_percent, 'cpu_used_percent': cpu_used_percent}
        data_to_send = dumps(data)
        sock.sendall(data_to_send.encode(encoding='utf_8'))
        return_message = sock.recv(1024).decode('utf_8')
        if return_message != 'OK':
            print("Nie udało się przesłać danych na serwer.")
        else:
            sock.close()
        sleep(INTERVAL_IN_SEC)

except Exception as e:
    raise e
