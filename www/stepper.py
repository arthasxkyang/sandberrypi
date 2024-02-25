import serial


class Stepper:
    def __init__(self, port, bdr):
        self.port = port
        self.bdr = bdr
        self.Ser = serial.Serial(port, bdr, timeout=1)
        self.cmdbuffer = [
            0x55, 0x01, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00
        ]
        self.reboot_cmd = [
            0x55, 0x03, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00
        ]
        self.rst_cmd = [
            0x55, 0x03, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00
        ]

    def reset(self):
        self.Ser.write(self.rst_cmd)
        while True:
            result = self.Ser.readline()
            if 'OK' in result:
                break

    def reboot(self):
        self.Ser.write(self.reboot_cmd)
        while True:
            result = self.Ser.readline()
            if 'OK' in result:
                break

    def move(self, x, y):
        #将x拆分为两个字节
        x1 = x >> 8
        x2 = x & 0xff
        #将y拆分为两个字节
        y1 = y >> 8
        y2 = y & 0xff
        #将x1,x2,y1,y2放入cmdbuffer
        self.cmdbuffer[2] = x1
        self.cmdbuffer[3] = x2
        self.cmdbuffer[5] = y1
        self.cmdbuffer[6] = y2

        self.Ser.write(self.cmdbuffer)
        while True:
            result = self.Ser.readline()
            if 'OK' in result:
                break
