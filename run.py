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
            data = input('Enter the com port: ')

            if data.isalpha():
                print('Uncorrect com port number !\nYou may enter only digits !\nTry again')
            elif data.isdigit():
                self.port = 'COM{}'.format(data)
                print(self.port)
                self.flag_set_com = False
            else:
                print('Somthing was wrong !\nTry again')

    def set_baud(self):
        while self.flag_set_baud:
            data = input('Enter the baud: ')

            if data.isalpha():
                print('Uncorrect baud !\nYou may enter only digits !\nTry again')
            elif data.isdigit():
                self.baud = data
                print(self.baud)
                self.flag_set_baud = False
            else:
                print('Somthing was wrong !\nTry again')

    def set_current_dis(self):
        while self.flag_set_current_dis:
            data = input('Enter discharge current: ')

            if data.isalpha():
                print('Uncorrect discharge current !\nYou may enter only digits !\nTry again')
            elif data.isdigit():
                self.discharge_current = data
                print(self.discharge_current)
                self.flag_set_current_dis = False
            else:
                print('Somthing was wrong !\nTry again')

    def set_bat_name(self):
        while self.flag_set_bat_name:
            data = input('Enter the battery name: ')

            if data:
                self.battery_name = data
                print(self.battery_name)
                self.flag_set_bat_name = False
            else:
                print('Somthing was wrong !\nTry again')

    def db_init(self):
        self.db_name = '{} {}'.format(self.battery_name, time.time())
        self.db_conn, self.db_cursor = db.init_db(self.db_name)
        db.create_table_head_data_in_db(self.db_cursor)
        db.create_table_in_db(self.db_cursor)
        db.commit_changes(self.db_conn)

    def db_head_data(self):
        db.insert_into_head_data(self.db_cursor, self.battery_name, self.discharge_current, time.time(), datetime.now())
        db.select_from_db(self.db_cursor, name_table_in_db='head_data')
        db.commit_changes(self.db_conn)

    def serial_connect(self):
        self.class_serial_start = SerialStart(port=self.port, baud=self.baud)

        if self.class_serial_start.connect_to_port():
            print('con good')

        self.thread_for_serial = Thread4Serial(self.call_back_from_serial, self.class_serial_start.serial_port,
                                               self.db_name)
        self.thread_for_serial.go_go()

    def serial_disconnect(self):
        self.thread_for_serial.terminate()
        while self.thread_for_serial.isAlive():
            pass
        if self.class_serial_start.disconnect_from_port():
            print('discon good')

    def cmd_run(self):
        while self.__cmd_run:
            data_cmd = input('Enter command -> ')
            print(data_cmd)

            if data_cmd == 'exit':
                self.serial_disconnect()
                self.__cmd_run = False
            elif data_cmd == 'reda_db':
                db.select_from_db(self.db_cursor, name_table_in_db='battery_data')


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
    sys.exit(0)



