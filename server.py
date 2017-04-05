#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

from json import loads
from conn_to_db import connect_with_db, insert_to_db

insert_sql = "insert into cpu_memory_usage_data(cpu_percent_of_usage, memory_percent_of_usage, ip_address) values(%s, %s, '%s');"

db = connect_with_db()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('0.0.0.0', 50000)
print('Pod IP %s otwieram port %s' % server_address)
sock.bind(server_address)

sock.listen(5)
print('Czekam na połączenie.')

while True:
    try:
        connection, client_address = sock.accept()
        print('Połączenie od:', client_address[0])
        data = connection.recv(1024)
        if data:
            data = loads(data.decode("utf-8"))
            print("Użycie procesora: %s%%, użycie pamięci: %s%%, IP: %s" % (data['cpu_used_percent'], data['memory_used_percent'], client_address[0]))
            cpu_mem_data = (data['cpu_used_percent'], data['memory_used_percent'], client_address[0])
            try:
                insert_to_db(cpu_mem_data, db, insert_sql)
                return_message = 'OK'
            except Exception as e:
                print("Nieudane zapisanie do bazy danych %s" % e)
                return_message = 'ERR'
            connection.sendall(return_message.encode(encoding='utf_8'))
    except Exception as e:
        connection.close()
        raise e

db.close()
