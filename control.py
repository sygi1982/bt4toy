import serial
from time import sleep

class control:

    def __init__(self, port):
        self.port = port
        self.out = serial.Serial(port, 115200, timeout=0)

    def __del__(self):
        self.out.close()

    def turnleft(self):
        self.out.write('0p0100000000')

    def turnrigth(self):
        self.out.write('0p0200000000')

    def forward(self, power):
        self.out.write('0p0400ff0000')

    def backward(self, power):
        self.out.write('0p0800ff0000')


if __name__ == "__main__":
    port = "/dev/rfcomm0"
    ctrl = control(port)
    ctrl.forward(100)
    ctrl.turnrigth()
    sleep(1)
    ctrl.turnleft()
    ctrl.backward(100)
    sleep(1)
