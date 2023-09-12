import subprocess
import sys

import serial


class ConfigManager:
    def __init__(self):
        self.serial = None
        self.port = 'COM10'
        self.baudrate = 9600
        self.timeout = None
        self.ports = []
        self.ports_num = 0

    def upgrade_ports(self):
        try:
            result = subprocess.check_output(["python", "-m", "serial.tools.list_ports"],
                                             text=True, stderr=subprocess.PIPE)
            port_list = result.split("\n")
            new_values = [line.split()[0] for line in port_list if line.strip()]
        except subprocess.CalledProcessError:
            new_values = []
        self.ports = new_values
        return self.ports

    def set_serial(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.serial = serial.Serial()
        self.serial.port = self.port
        self.serial.baudrate = self.serial.baudrate
        self.serial.timeout = self.timeout

    def serial_is_open(self):
        try:
            self.serial.open()
            return True, None
        except serial.SerialException as error:
            sys.excepthook(type(error), error, error.__traceback__)
            return False, error
