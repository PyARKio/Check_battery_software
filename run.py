# -- coding: utf-8 --
from __future__ import unicode_literals
import sys
import serial
import time
from datetime import datetime
from Drivers.log_settings import log
from Drivers.lib_serial import SerialStart
from Drivers.lib_serial import Thread4Serial
from Drivers import db


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"

log.info('Starting of check_battery_capacity')

port = 'COM13'
baud = 38400


class CheckBatteryCapacity(object):
    def __init__(self):
        log.info('__init__')
        self.__cmd_run = True

        self.flag_set_com = True
        self.flag_set_baud = True
        self.flag_set_current_dis = True
        self.flag_set_bat_name = True

        self.port = None
        self.baud = None
        self.discharge_current = None
        self.battery_name = None

        self.class_serial_start = None
        self.thread_for_serial = None

        self.db_conn = None
        self.db_cursor = None
        self.db_name = None

        # self.commands = {'exit': Command_handler._handler_exit,
        #                  '-q': Command_handler._handler_exit,
        #
        #                  'connect to other mqtt broker': Command_handler._handler_reconnect,
        #                  '-R': Command_handler._handler_reconnect,
        #
        #                  'HELP': Command_handler._handler_help,
        #                  '-h': Command_handler._handler_help,
        #
        #                  'system state': Command_handler._handler_sys_state,
        #                  '-ss': Command_handler._handler_sys_state,
        #
        #                  'table of sensors': Command_handler._handler_table_sensors,
        #                  '-t': Command_handler._handler_table_sensors,
        #
        #                  'reboot sensors': Command_handler._handler_reboot_sensor,
        #                  '-r': Command_handler._handler_reboot_sensor,
        #
        #                  'radio statistics': Command_handler._handler_radio_statistics,
        #                  '-rst': Command_handler._handler_radio_statistics,
        #
        #                  'print history': Command_handler._handler_history,
        #                  '-ph': Command_handler._handler_history,
        #
        #                  'sensor data': Command_handler._handler_sensors_data,
        #                  '-sd': Command_handler._handler_sensors_data,
        #
        #                  'plot data': Command_handler._handler_plot_data,
        #                  '-pd': Command_handler._handler_plot_data,
        #
        #                  '-psd': Command_handler._handler_plot_some_data,
        #
        #                  '-p1c': Command_handler._handler_plot_data_for_bot,
        #
        #                  '-p2c': Command_handler._handler_plot_2_data_for_bot,
        #
        #                  }

    # ******************************************
    def call_back_from_serial(self, data):
        pass
        # print('DATA from serial:\n{}'.format(data))
        # if 'V' in data:
        #     db.insert_into_db(self.db_cursor, time.time(), datetime.now(), data.split('V')[1])
    # ******************************************

    def set_com_port(self):
        while self.flag_set_com:
            log.info('Enter the com port')
            data = input('Enter the com port: ')

            if data.isalpha():
                log.info('Uncorrect com port number !\nYou may enter only digits !\nTry again')
            elif data.isdigit():
                self.port = 'COM{}'.format(data)
                log.info('User entered {}'.format(self.port))
                self.flag_set_com = False
            else:
                log.info('Something was wrong !\nTry again')

    def set_baud(self):
        while self.flag_set_baud:
            log.info('Enter the baud')
            data = input('Enter the baud: ')

            if data.isalpha():
                log.info('Uncorrect baud !\nYou may enter only digits !\nTry again')
            elif data.isdigit():
                self.baud = data
                log.info('User entered {}'.format(self.baud))
                self.flag_set_baud = False
            else:
                log.info('Somthing was wrong !\nTry again')

    def set_current_dis(self):
        while self.flag_set_current_dis:
            log.info('Enter discharge current')
            data = input('Enter discharge current: ')

            if data.isalpha():
                log.info('Uncorrect discharge current !\nYou may enter only digits !\nTry again')
            elif data.isdigit():
                self.discharge_current = data
                log.info('Discharge current is {}'.format(self.discharge_current))
                self.flag_set_current_dis = False
            else:
                log.info('Somthing was wrong !\nTry again')

    def set_bat_name(self):
        log.info('Enter the battery name')
        while self.flag_set_bat_name:
            data = input('Enter the battery name: ')

            if data:
                self.battery_name = data
                log.info('Battery name is {}'.format(self.battery_name))
                self.flag_set_bat_name = False
            else:
                log.info('Somthing was wrong !\nTry again')

    def db_init(self):
        self.db_name = '{} {}'.format(self.battery_name, time.time())
        log.info('DB name: {}'.format(self.db_name))

        self.db_conn, self.db_cursor = db.init_db(self.db_name)
        log.info('DB_conn: {}\nDB_cursor: {}'.format(self.db_conn, self.db_cursor))

        if self.db_conn and self.db_cursor:
            if not db.create_table_head_data_in_db(self.db_cursor):
                print('Can not create table <head_data>')
                self.serial_disconnect()
                log.info('SYSTEM STOP')
                sys.exit(0)
            if not db.create_table_in_db(self.db_cursor):
                print('Can not create table <battery_data>')
                self.serial_disconnect()
                log.info('SYSTEM STOP')
                sys.exit(0)
            if not db.commit_changes(self.db_conn):
                print('Can not commit')
                self.serial_disconnect()
                log.info('SYSTEM STOP')
                sys.exit(0)
        else:
            print('Can not init db')
            self.serial_disconnect()
            log.info('SYSTEM STOP')
            sys.exit(0)

    def db_head_data(self):
        if not db.insert_into_head_data(self.db_cursor, self.battery_name, self.discharge_current, time.time(), datetime.now()):
            print('Can not insert in db {} {} {} {}'.
                  format(self.battery_name, self.discharge_current, time.time(), datetime.now()))
            self.serial_disconnect()
            log.info('SYSTEM STOP')
            sys.exit(0)
        if not db.select_from_db(self.db_cursor, name_table_in_db='head_data'):
            print('Can not select from table <head_data>')
            self.serial_disconnect()
            log.info('SYSTEM STOP')
            sys.exit(0)
        if not db.commit_changes(self.db_conn):
            print('Can not commit')
            self.serial_disconnect()
            log.info('SYSTEM STOP')
            sys.exit(0)

    def serial_connect(self):
        self.class_serial_start = SerialStart(port=self.port, baud=self.baud)

        if not self.class_serial_start.connect_to_port():
            print('Can not connect to {}'.format(self.port))
            self.serial_disconnect()
            log.info('SYSTEM STOP')
            sys.exit(0)

        self.thread_for_serial = Thread4Serial(self.call_back_from_serial, self.class_serial_start.serial_port,
                                               self.db_name)
        self.thread_for_serial.go_go()

    def serial_disconnect(self):
        self.thread_for_serial.terminate()
        timeout = time.time()
        while self.thread_for_serial.isAlive() and time.time() - timeout < 10:
            pass
        if not self.class_serial_start.disconnect_from_port():
            print('Could not disconnect from port')

    def cmd_run(self):
        while self.__cmd_run:
            data_cmd = input('Enter command -> ')
            log.info('Enter command -> {}'.format(data_cmd))

            if data_cmd == 'exit':
                self.serial_disconnect()
                self.__cmd_run = False
            elif data_cmd == 'read_db':
                db.select_from_db(self.db_cursor, name_table_in_db='battery_data')
            elif data_cmd == 'start print':
                self.thread_for_serial._print = True
            elif data_cmd == 'stop print':
                self.thread_for_serial._print = False
            elif data_cmd == 'capacity':
                data = db.select_from_db(self.db_cursor, name_table_in_db='battery_data', param='volt')
                if not data:
                    print('Can not select from table <battery_data>')
                    # self.serial_disconnect()
                    # log.info('SYSTEM STOP')
                    # sys.exit(0)


def main():
    serial_port = serial.Serial(port=port,
                                baudrate=baud,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS)

    while 1:
        # if self.flag_work:
        try:
            temp = serial_port.readline()
        except Exception as err:
            print('Не удалось прочитать из COM порта {}'.format(err))
            return
        else:
            # print(temp)
            try:
                temp = (temp.decode('ascii')).strip()
            except Exception as err:
                print('Не удалось декодировать в "ascii" {}'.format(err))
            else:
                print('{} {}'.format(datetime.now(), temp))


if __name__ == '__main__':
    # main()
    print(sys.version)
    con = CheckBatteryCapacity()
    con.set_com_port()
    con.set_baud()
    con.set_current_dis()
    con.set_bat_name()
    con.db_init()
    con.db_head_data()
    con.serial_connect()
    # con.serial_disconnect()
    con.cmd_run()

    print('SYSTEM STOP')
    log.info('SYSTEM STOP')
    sys.exit(0)



