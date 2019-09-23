# -- coding: utf-8 --
from __future__ import unicode_literals
import serial
from datetime import datetime
import threading
from Drivers import db
import time
from Drivers.log_settings import log
import sys


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
        log.info('Try connect to serial port {}'.format(self.port))
        try:
            self.serial_port = serial.Serial(port=self.port,
                                             baudrate=self.baud,
                                             parity=serial.PARITY_NONE,
                                             stopbits=serial.STOPBITS_ONE,
                                             bytesize=serial.EIGHTBITS)
        except Exception as err:
            print('Could not open port {}'.format(self.port))
            log.error(err)
            return False
        else:
            log.info('Connect to Serial-port:  OK')
            return True

    def disconnect_from_port(self):
        try:
            self.serial_port.close()
        except Exception as err:
            print('Could not disconnect from port {}'.format(self.port))
            log.error(err)
            return False
        else:
            log.info('Disconnect from port:  OK')
            return True

    def send_to_port(self, message):
        try:
            self.serial_port.write(message)
        except Exception as err:
            print('Could send {} to port {}'.format(message, self.port))
            log.error(err)
            return False
        else:
            log.info('Send {} to port {}: successfully'.format(message, self.port))
            return True


class Thread4Serial(threading.Thread):
    def __init__(self, callback_handler, serial_port_as_obj, db_name):
        threading.Thread.__init__(self)
        self._running = True
        self.__handler = callback_handler
        self.serial_port = serial_port_as_obj
        self._pause = False
        self._print = False

        self.db_conn = None
        self.db_cursor = None
        self.db_name = db_name

    def terminate(self):
        log.info('Terminate')
        self._running = False

    def go_go(self):
        log.info('Run')
        self._running = True
        self.start()

    def run(self):
        self.db_conn, self.db_cursor = db.init_db(self.db_name)
        log.info('Thread was run')
        while self._running:
            try:
                data = self.serial_port.readline()
            except Exception as err:
                log.error('Can not read from port {}'.format(err))
            else:
                try:
                    data = (data.decode('ascii')).strip()
                except Exception as err:
                    log.error('Can not decode in "ascii" {}'.format(err))
                else:
                    if self._print:
                        print('{} {}'.format(datetime.now(), data))
                    self.__handler(data)
                    if 'V' in data:
                        if not db.insert_into_db(self.db_cursor, time.time(), datetime.now(), int(data.split('V')[1])):
                            print('Can not insert in db {} {} {}'.
                                  format(time.time(), datetime.now(), int(data.split('V')[1])))
                            sys.exit(0)
                        if not db.commit_changes(self.db_conn):
                            print('Can not commit')
                            sys.exit(0)




