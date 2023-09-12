import sys

from Window import Window
import time


class GUI:
    def __init__(self, _app):
        self.app = _app
        self.window = None
        self.read = False
        self.stream = None

        # WINDOW buttons and variables
        self.COM = 'None'
        self.baudrate = 9600
        self.timeout = 1
        self.plotter = False
        self.auto_scroll = False
        self.mode = 'default'
        self.Files = None
        self.stop = True
        self.data_read = 0

    def send_data(self, data):
        try:
            self.app.send_data(data)
        except Exception as e:
            sys.excepthook(type(e), e, e.__traceback__)

    def connection_enable(self, stream):
        print(f'\n<Connected Successfully!\tPort: {self.COM}, Baudrate: {self.baudrate}>')
        self.data_read = 0
        self.stop = False
        self.stream = stream

    def start_read(self):
        print("\n<communication started!>\n")
        self.read = True
        self.app.serial.flush()
        self.app.start_read_byte()
        # read data in loop
        try:
            while self.read:
                self.app.read_data()
                if len(self.stream.data) > self.data_read:
                    if self.stream.plot:
                        x = self.stream.data[-2]
                        y = self.stream.data[-1]
                        self.window.mid_frame.plot_widget.plot(x, y)
                        self.data_read += 2
                        self.stream.plot = False
                    else:
                        data = self.stream.data[-1]
                        print(data, end='')
                        self.data_read += 1
        except Exception as e:
            sys.excepthook(type(e), e, e.__traceback__)

    def stop_read(self):
        self.read = False

    def connection_unenable(self, error_message):
        self.stop_read()
        # print(error_message)
        # print('connection not possible...\n')

    def connection_stop(self):
        self.read = False
        self.stop = True
        self.data_read = 0

    def create_window(self):
        self.window = Window(self)
        self.window.protocol("WM_DELETE_WINDOW", self.disconnect)
        self.window.mainloop()

    def connect(self):
        self.read = False
        self.window.mid_frame.options_menu.state = False
        self.window.mid_frame.options_menu.stop_button_event()
        time.sleep(1)
        if self.app.serial.serial is not None:
            self.app.serial.serial.close()

        # self.read = True
        self.app.connect(self.COM, self.baudrate, self.timeout)

    def disconnect(self):
        if self.read:
            self.window.open_toplevel()
        else:
            self.app.disconnect()
            self.window.destroy()

    def set_COM(self, com):
        self.COM = com

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_ports(self):
        return self.app.manager.upgrade_ports()
