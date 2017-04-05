#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import argv
from conn_to_db import read_from_db, connect_with_db

canCount = False


def does_ip_exists_in_table(ip, period_in_minutes, db):
    count_sql = "select count(1) as count from cpu_memory_usage_data where ip_address = '%s'" % ip
    count_rec = read_from_db(count_sql, db)
    result = ''
    for (count) in count_rec:
        if count[0] == 0:
            result = "Nie znaleziono danych dla podanego adresu IP: '%s'" % ip
        else:
            result = "Brak danych z ostatnich %s minut." % period_in_minutes
    return result


if len(argv) != 4:
    raise ValueError("Nieprawidłowa liczba argumentów:(czas w minutach, typ zasobu(CPU, MEMORY), adres IP)")

period_in_minutes, resource_type, ip = argv[1:]

if not period_in_minutes.isdigit():
    raise ValueError("Dopuszczalna wartość pierwszego argumentu to liczba całkowita. (Czas do wyliczenia średniej w minutach)")
if resource_type.lower() not in ('cpu', 'memory'):
    raise ValueError("Dopuszczalne wartości drugiego argumentu to: 'CPU' lub 'MEMORY'")

sql = """select avg(%s_percent_of_usage) as avg from cpu_memory_usage_data
         where created > (select now()) - interval %s minute
         and ip_address = '%s';""" % (resource_type.lower(), period_in_minutes, ip)

db = connect_with_db()
result = read_from_db(sql, db)

if resource_type.lower() == 'cpu':
    for (avg) in result:
        if avg[0] is None:
            print(does_ip_exists_in_table(ip, period_in_minutes, db))
        else:
            print("Średnie użycie procesora to %s%% w ostatnich %s minutach." % (round(avg[0], 2), period_in_minutes))
else:
    for (avg) in result:
        if avg[0] is None:
            print(does_ip_exists_in_table(ip, period_in_minutes, db))
        else:
            print("Średnie użycie pamięci to %s%% w ostatnich %s minutach." % (round(avg[0], 2), period_in_minutes))

db.close()
