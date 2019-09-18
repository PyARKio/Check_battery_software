# -- coding: utf-8 --
from __future__ import unicode_literals
import sqlite3


def init_db(name_db):
    try:
        conn = sqlite3.connect('{}.db'.format(name_db))  # или :memory: чтобы сохранить в RAM
    except Exception as err:
        print(err)
        return 0
    else:
        cursor = conn.cursor()
        return conn, cursor


def get_metadata(conn, cursor):
    # cursor.execute("CREATE DATABASE {} ;".format('test2'))
    print(conn.get_dsn_parameters(), "\n")
    cursor.execute("SELECT version();")
    # cursor.execute("SELECT all;")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")


def create_table_head_data_in_db(cursor):
    # Execute a command: this creates a new table
    try:
        cursor.execute("CREATE TABLE head_data ("
                       "battery_name varchar, "
                       "discharge_current varchar, "
                       "start_at_in_sec timestamp, "
                       "start_at_in_date timestamp);")
    except Exception as err:
        print('Error while creating PostgreSQL table: {}'.format(err))


def create_table_in_db(cursor):
    # Execute a command: this creates a new table
    try:
        cursor.execute("CREATE TABLE battery_data ("
                       "id serial PRIMARY KEY, "
                       "time_sec timestamp, "
                       "time_in_date timestamp, "
                       "volt varchar);")
    except Exception as err:
        print('Error while creating PostgreSQL table: {}'.format(err))


def insert_into_head_data(cursor, bat_name, dis, in_sec, in_date):
    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    # cursor.execute("INSERT INTO test_db (num, data) VALUES (%s, %s)", (123478, "passwd"))
    cursor.execute("INSERT INTO head_data ("
                   "battery_name, "
                   "discharge_current, "
                   "start_at_in_sec, "
                   "start_at_in_date) VALUES(?, ?, ?, ?)", (bat_name, str(dis), in_sec, in_date))


def insert_into_db(cursor, in_sec, in_date, volt):
    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    # cursor.execute("INSERT INTO test_db (num, data) VALUES (%s, %s)", (123478, "passwd"))
    cursor.execute("INSERT INTO battery_data ("
                   "time_sec, "
                   "time_in_date, "
                   "volt) VALUES(?, ?, ?)", (in_sec, in_date, volt))


def select_from_db(cursor, name_table_in_db, param='*'):
    # Query the database and obtain data as Python objects
    cursor.execute("SELECT {} FROM {};".format(param, name_table_in_db))
    data = cursor.fetchall()
    print(len(data))

    for line in data:
        print(line)


def delete_from_table_in_db(cursor, name_table_in_db, key, value):
    # sql = 'DELETE FROM {} WHERE {} = {}'.format(name_table_in_db, key, value)
    # cursor.execute(sql)
    cursor.execute("DELETE FROM test_db WHERE num = 1234")


def commit_changes(conn):
    # Make the changes to the database persistent
    conn.commit()


def disconnect_from_db(conn, cursor):
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")


def select_all_table():
    cursor.execute("""SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'public'""")
    for table in cursor.fetchall():
        print(table)