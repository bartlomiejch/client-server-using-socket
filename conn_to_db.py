#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from MySQLdb import connect

DBHOST = 'localhost'
USER = 'root'
PASSWD = 'passwd'
DATABASE = 'events'


def read_from_db(sql_query, db):
    '''select data from database'''
    try:
        cursor = db.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
    except Exception as e:
        print("Nie udało się połączyć z bazą danych: %s" % e)
        raise e
    return result


def insert_to_db(cpu_mem_data, db, sql):
    '''insert data to database'''
    cursor = db.cursor()
    cursor.execute(sql % cpu_mem_data)
    cursor.close()
    db.commit()
    return


def connect_with_db():
    '''connect to database'''
    try:
        db = connect(host=DBHOST, user=USER, passwd=PASSWD, db=DATABASE)
    except Exception as e:
        print("Nie udało się połączyć z bazą danych: '%s'" % e)
        raise e
    return db
