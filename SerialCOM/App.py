from Comunication import Communication
from GUI import GUI
from DataCollection import DataCollection
from ConfigManager import ConfigManager


class App:
    def __init__(self):
        self.gui = GUI(self)
        self.serial = Communication()
        self.data = DataCollection()
        self.manager = ConfigManager()

        self.init_GUI()

    def init_GUI(self):
        self.gui.create_window()

    def connect(self, port, baudrate, timeout):
        self.manager.set_serial(port, baudrate, timeout)
        is_open, message = self.manager.serial_is_open()
        if message == "x":
            return
        if is_open:
            self.serial.start_connection(self.manager.serial)
            self.data.make_stream()
            self.serial.set_output(self.data.stream)
            self.gui.connection_enable(self.data.stream)
        else:
            self.gui.connection_unenable(message)

    def disconnect(self):
        self.gui.connection_stop()
        self.serial.close_connection()
        self.data.save_last_transmission()

    def start_read_byte(self):
        self.serial.read = True
        # get type of data
        self.serial.read_byte()
        # get size of data
        self.serial.read_byte()

    def read_data(self):
        self.serial.read_byte()

    def send_data(self, data):
        self.serial.write(data)

    def get_data(self, index):
        return self.data.get_data(index)

    def close(self):
        self.disconnect()
        self.data.save_all()
