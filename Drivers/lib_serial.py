# -- coding: utf-8 --
from __future__ import unicode_literals
import serial
from datetime import datetime
import threading
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
    def __init__(self, callback_handler, periodic):
        threading.Thread.__init__(self)
        self._running = True
        self.__handler = callback_handler
        self.__time = periodic
        self._pause = False

    def terminate(self):
        self._running = False

    def go_go(self):
        self._running = True
        self.start()

    def run(self):
        while self._running:
            time.sleep(self.__time)
            if not self._pause:
                self.__handler()




