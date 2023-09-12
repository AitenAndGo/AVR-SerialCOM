import struct


class DataCollection:

    def __init__(self):
        self.stream = None
        self.data = []

    def make_stream(self):
        # create a stream 
        self.stream = Stream()
        self.data.append(Stream)

    def save_last_transmission(self):
        pass

    def get_data(self, index):
        pass

    def save_all(self):
        pass


class Stream:

    def __init__(self):
        # all read bytes
        self.encrypted_data = []
        # all variable data read
        self.data = []
        self.type = 'byte'
        self.plot = False
        # number of read elements
        self.size_of_data = 0
        # number of bytes
        self.len_of_data_type = 1
        # new bytes
        self.bytes = []
        self.variable = None

    def set_type(self, _type):
        self.type = _type

    def push(self, byte):

        # print(byte)

        if self.type == 'plot':
            self.type = None
            self.encrypted_data.clear()

        self.encrypted_data.append(byte)
        # print("byte: ", byte)
        if len(self.encrypted_data) > (self.size_of_data + 1) and len(self.encrypted_data) != 2:
            self.encrypted_data.clear()

        if len(self.encrypted_data) == 1:
            self.set_type(self.get_type(self.encrypted_data[0]))
        elif len(self.encrypted_data) == 2:
            self.set_size_of_data(self.encrypted_data[1])
        else:
            self.decode(byte)

    def get_type(self, type_byte):
        if type_byte == b'b':
            self.len_of_data_type = 1
            return 'byte'
        if type_byte == b'c':
            self.len_of_data_type = 1
            return 'char'
        # todo:
        # so when u want to plot u send 'p' and then type and two arguments x and y
        if type_byte == b'p':
            self.plot = True
            return 'plot'
        if type_byte == b'i':
            self.len_of_data_type = 2
            self.variable = int(0)
            return 'int'
        if type_byte == b'f':
            self.len_of_data_type = 4
            self.variable = float(0)
            return 'float'
        if type_byte == b's':
            self.len_of_data_type = 2
            self.variable = 0
            return 'uint16_t'
        if type_byte == b'u':
            self.len_of_data_type = 1
            self.variable = 0
            return 'uint8_t'

    def decode(self, byte):
        if self.type == 'byte':
            self.data.append(ord(byte))
        elif self.type == 'char':
            self.data.append(byte.decode('utf-8'))
        elif self.type == 'uint16_t':
            self.bytes.append(byte)
            if len(self.bytes) == self.len_of_data_type:
                binary_string = b''.join(self.bytes)
                self.variable = struct.unpack('<H', binary_string)
                self.data.append(self.variable[0])
                self.variable = None
                self.bytes.clear()
        elif self.type == 'uint8_t':
            self.bytes.append(byte)
            if len(self.bytes) == self.len_of_data_type:
                binary_string = b''.join(self.bytes)
                self.variable = struct.unpack('<B', binary_string)
                self.data.append(self.variable[0])
                self.variable = None
                self.bytes.clear()
        elif self.type == 'int':
            self.bytes.append(byte)
            if len(self.bytes) == self.len_of_data_type:
                binary_string = b''.join(self.bytes)
                self.variable = struct.unpack('<h', binary_string)
                self.data.append(self.variable[0])
                self.variable = None
                self.bytes.clear()
        elif self.type == 'float':
            self.bytes.append(byte)
            if len(self.bytes) == self.len_of_data_type:
                binary_string = b''.join(self.bytes)
                self.variable = struct.unpack('<f', binary_string)
                self.data.append(self.variable[0])
                self.variable = None
                self.bytes.clear()

    def set_size_of_data(self, byte):
        # number of bytes
        self.size_of_data = ord(byte)
