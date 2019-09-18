# -- coding: utf-8 --
from __future__ import unicode_literals
import sqlite3
from Drivers.log_settings import log


def init_db(name_db):
    try:
        conn = sqlite3.connect('{}.db'.format(name_db))  # или :memory: чтобы сохранить в RAM
    except Exception as err:
        log.error(err)
        return False, False
    else:
        log.info('Init db <{}>: successfully'.format(name_db))
        try:
            cursor = conn.cursor()
        except Exception as err:
            log.error(err)
            return False, False
        else:
            log.info('Create cursor for db <{}>: successfully'.format(name_db))
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
                       "discharge_current int, "
                       "start_at_in_sec timestamp, "
                       "start_at_in_date timestamp);")
    except Exception as err:
        log.error(err)
        return False
    else:
        log.info('Create table <head_data>: successfully')
        return True


def create_table_in_db(cursor):
    # Execute a command: this creates a new table
    try:
        cursor.execute("CREATE TABLE battery_data ("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "time_sec timestamp, "
                       "time_in_date timestamp, "
                       "volt int);")
    except Exception as err:
        log.error(err)
        return False
    else:
        log.info('Create table <battery_data>: successfully')
        return True


def insert_into_head_data(cursor, bat_name, dis, in_sec, in_date):
    try:
        cursor.execute("INSERT INTO head_data ("
                       "battery_name, "
                       "discharge_current, "
                       "start_at_in_sec, "
                       "start_at_in_date) VALUES(?, ?, ?, ?)", (bat_name, str(dis), in_sec, in_date))
    except Exception as err:
        log.error(err)
        return False
    else:
        log.info('Insert in table <head_data> {} {} {} {}: successfully'.format(bat_name, str(dis), in_sec, in_date))
        return True


def insert_into_db(cursor, in_sec, in_date, volt):
    try:
        cursor.execute("INSERT INTO battery_data ("
                       "time_sec, "
                       "time_in_date, "
                       "volt) VALUES(?, ?, ?)", (in_sec, in_date, volt))
    except Exception as err:
        log.error(err)
        return False
    else:
        return True


def select_from_db(cursor, name_table_in_db, param='*'):
    try:
        cursor.execute("SELECT {} FROM {};".format(param, name_table_in_db))
    except Exception as err:
        print(err)
        log.error(err)
        return False
    else:
        try:
            data = cursor.fetchall()
        except Exception as err:
            print(err)
            log.error(err)
            return False
        else:
            log.info('Select {} from table {}: successfully'.format(param, name_table_in_db))
            print(len(data))
            print(data)

            # for line in data:
            #     print(line)

            return data


def delete_from_table_in_db(cursor, name_table_in_db, key, value):
    # sql = 'DELETE FROM {} WHERE {} = {}'.format(name_table_in_db, key, value)
    # cursor.execute(sql)
    cursor.execute("DELETE FROM test_db WHERE num = 1234")


def commit_changes(conn):
    # Make the changes to the database persistent
    try:
        conn.commit()
    except Exception as err:
        log.error(err)
        return False
    else:
        log.info('Commit: successfully')
        return True


def disconnect_from_db(conn, cursor):
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")


def select_all_table(cursor):
    cursor.execute("""SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'public'""")
    for table in cursor.fetchall():
        print(table)



