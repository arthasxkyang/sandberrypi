from serial import Serial


class Stepper:
    def __init__(self, port, bdr):
        self.port = port
        self.bdr = bdr
        self.Ser = Serial(port, bdr, timeout=1)
        self.cmdbuffer = [
            0x55, 0x01, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00
        ]
        self.reboot_cmd = [
            0x55, 0x03, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00
        ]
        self.rst_cmd = [
            0x55, 0x02, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00
        ]

    def home(self):
        self.Ser.flush()
        print("stepper -----      Homing")
        self.Ser.write(self.rst_cmd)
        while True:
            result = self.Ser.readline()
            print(result)
            if 'O'.encode() or 'K'.encode() in result:
                print('im here')
                return True

    def reboot(self):
        self.Ser.flush()
        print("stepper -----      Rebooting")
        self.Ser.write(self.reboot_cmd)
        while True:
            result = self.Ser.readline()
            if 'O'.encode() or 'K'.encode() in result:
                break

    def move(self, x, y, t=1000):
        self.Ser.flush()
        # print("stepper -----      Moving")
        # print(f"x= {x},y= {y},t= {t}")
        drx = 0
        if x < 0:
            x = -x
            drx = 0
        else:
            drx = 1
        dry = 0
        if y < 0:
            y = -y
            dry = 0
        else:
            dry = 1

        # 将x拆分为两个字节
        x1 = x >> 8
        x2 = x & 0xff
        # 将y拆分为两个字节
        y1 = y >> 8
        y2 = y & 0xff
        # 将t拆分为两个字节
        t1 = t >> 8
        t2 = t & 0xff

        # 将x1,x2,y1,y2放入cmdbuffer
        self.cmdbuffer[2] = x1
        self.cmdbuffer[3] = x2
        self.cmdbuffer[4] = drx
        self.cmdbuffer[5] = y1
        self.cmdbuffer[6] = y2
        self.cmdbuffer[7] = dry
        self.cmdbuffer[8] = t1
        self.cmdbuffer[9] = t2

        self.Ser.write(self.cmdbuffer)
        while True:
            result = self.Ser.readline()
            print(result)
            if 'O'.encode() or 'K'.encode() in result:
                return True


if __name__ == '__main__':
    step = Stepper('COM22', 115200)
    if step.home():
        print('reset success')
    step.move(10000, 5000, 1000)
