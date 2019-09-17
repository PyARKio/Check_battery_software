# -- coding: utf-8 --
from __future__ import unicode_literals
import serial
from datetime import datetime
import threading
from Drivers import db
import time


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


class SerialStart:
    def __init__(self, port, baud):

        self.serial_port = None

        self.port = port
        self.baud = baud
        self.first_flag = 1

    def connect_to_port(self):
        print('Try connect to serial port {}'.format(self.port))
        try:
            self.serial_port = serial.Serial(port=self.port,
                                             baudrate=self.baud,
                                             parity=serial.PARITY_NONE,
                                             stopbits=serial.STOPBITS_ONE,
                                             bytesize=serial.EIGHTBITS)
        except Exception as err:
            print('Could not open port {}'.format(self.port))
            print(err)

            return False
        else:
            print('Connect to Serial-port:  OK')
            return True

    def disconnect_from_port(self):
        try:
            self.serial_port.close()
        except Exception as err:
            print('Could disconnect from port {}'.format(self.port))
            print(err)
            return False
        else:
            return True

    def send_to_port(self, message):
        try:
            self.serial_port.write(message)
        except Exception as err:
            print('Could send {} to port {}'.format(message, self.port))
            print(err)
            return False
        else:
            return True


class Thread4Serial(threading.Thread):
    def __init__(self, callback_handler, serial_port_as_obj, db_name):
        threading.Thread.__init__(self)
        self._running = True
        self.__handler = callback_handler
        self.serial_port = serial_port_as_obj
        self._pause = False

        self.db_conn = None
        self.db_cursor = None
        self.db_name = db_name

    def terminate(self):
        self._running = False

    def go_go(self):
        self._running = True
        self.start()

    def run(self):
        self.db_conn, self.db_cursor = db.init_db(self.db_name)
        print('Thread was run')
        while self._running:
            try:
                data = self.serial_port.readline()
            except Exception as err:
                print('Can not read from port {}'.format(err))
            else:
                try:
                    data = (data.decode('ascii')).strip()
                except Exception as err:
                    print('Can not decode in "ascii" {}'.format(err))
                else:
                    # print('{} {}'.format(datetime.now(), data))
                    # self.__handler(data)
                    if 'V' in data:
                        db.insert_into_db(self.db_cursor, time.time(), datetime.now(), data.split('V')[1])
                        db.commit_changes(self.db_conn)




