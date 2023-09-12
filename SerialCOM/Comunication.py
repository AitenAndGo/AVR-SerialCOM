class Communication:
    def __init__(self):
        self.serial = None
        self.byte = None
        self.output_stream = None

    def start_connection(self, serial):
        self.serial = serial

    def read_byte(self):
        # read from serial
        # while self.read:
        self.byte = self.serial.read(1)
        if self.byte != b'':
            self.output_stream.push(self.byte)

    def set_output(self, stream):
        self.output_stream = stream

    def write(self, data):
        # write to serial
        for byte in data:
            self.serial.write(byte.encode())

    def flush(self):
        self.serial.flush()

    def close_connection(self):
        if self.serial is not None:
            self.serial.close()
