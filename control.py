#/*******************************************************************************
#* Copyright (c) 2016 Grzegorz Sygieda
#*
#* Licensed under the Apache License, Version 2.0 (the "License");
#* you may not use this file except in compliance with the License.
#* You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#*******************************************************************************/

import serial
import sys
from time import sleep
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView

class Control(QObject):
    def __init__(self, port):
        super(Control, self).__init__()
        self.port = port
        self.out = serial.Serial(port, 115200, timeout=0)
        self.callback = []

    def __del__(self):
        self.out.close()

    def parsePower(self, power):
        self.power = int((power * 255) / 100)
        self.trail = self.power + 51
        if (self.trail > 255):
            self.trail = 255

    def flushCmd(self, cmd):
        print ('flushing ' + cmd)
        self.out.write(cmd.encode('utf-8'))

    # NOTE: calculate values according to bt snoop file
    @pyqtSlot()
    def idle(self):
        cmd = '0p0000002033'
        print ('idle')
        self.flushCmd(cmd)

    @pyqtSlot(int)
    def forward(self, power):
        self.parsePower(power)
        cmd = '0p0400' + '{:02x}'.format(self.power)
        cmd += '20' + '{:02x}'.format(self.trail)
        print ('forward ' + str(power))
        self.flushCmd(cmd)

    @pyqtSlot(int)
    def backward(self, power):
        self.parsePower(power)
        cmd = '0p0800' + '{:02x}'.format(self.power)
        cmd += '20' + '{:02x}'.format(self.trail)
        print ('backward ' + str(power))
        self.flushCmd(cmd)

    @pyqtSlot()
    def turnLeft(self):
        cmd = '0p01ff0020ff'
        print ('turn left')
        self.flushCmd(cmd)

    @pyqtSlot()
    def turnRight(self):
        cmd = '0p02ff0020ff'
        print ('turn right')
        self.flushCmd(cmd)

    @pyqtSlot(int)
    def forwardLeft(self, power):
        self.parsePower(power)
        cmd = '0p0500' + '{:02x}'.format(self.power)
        cmd += '20' + '{:02x}'.format(self.trail)
        print ('forward left ' + str(power))
        self.flushCmd(cmd)

    @pyqtSlot(int)
    def forwardRight(self, power):
        self.parsePower(power)
        cmd = '0p0600' + '{:02x}'.format(self.power)
        cmd += '20' + '{:02x}'.format(self.trail)
        print ('forward right ' + str(power))
        self.flushCmd(cmd)

    @pyqtSlot(int)
    def backwardLeft(self, power):
        self.parsePower(power)
        cmd = '0p0900' + '{:02x}'.format(self.power)
        cmd += '20' + '{:02x}'.format(self.trail)
        print ('backward left ' + str(power))
        self.flushCmd(cmd)

    @pyqtSlot(int)
    def backwardRight(self, power):
        self.parsePower(power)
        cmd = '0p0a00' + '{:02x}'.format(self.power)
        cmd += '20' + '{:02x}'.format(self.trail)
        print ('backward right ' + str(power))
        self.flushCmd(cmd)

if __name__ == "__main__":
    port = "/dev/rfcomm0"
    ctrl = Control(port)
    app = QApplication(sys.argv)
    view = QQuickView()
    view.setTitle('BMW Z4 control')
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.setSource(QUrl('QtUi/main.qml'))
    context = view.rootContext()
    context.setContextProperty("control", ctrl)

    view.show()
    app.exec_()
    sys.exit()
