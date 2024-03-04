import serial
port = 'COM22'
bdr = 115200
import time
rst_cmd = [0x05,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
Ser = serial.Serial(port,bdr,timeout=1)
while True:
    print(Ser.readline())
    Ser.write(rst_cmd)

