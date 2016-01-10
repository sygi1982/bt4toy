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

    @pyqtSlot()
    def idle(self):
        cmd = '0p0000002000'
        print ('idle')
        self.out.write(cmd.encode('utf-8'))

    @pyqtSlot(int)
    def left(self, power):
        power = (power * 255) / 100
        cmd = '0p01' + '{:02x}'.format(int(power)) + '0020' + '{:02x}'.format(int(power))
        print ('left ' + str(power) + ' ' + cmd)
        self.out.write(cmd.encode('utf-8'))

    @pyqtSlot(int)
    def right(self, power):
        power = (power * 255) / 100
        cmd = '0p02' + '{:02x}'.format(int(power)) + '0020' + '{:02x}'.format(int(power))
        print ('right ' + str(power) + ' ' + cmd)
        self.out.write(cmd.encode('utf-8'))

    @pyqtSlot(int)
    def forward(self, power):
        power = (power * 255) / 100
        cmd = '0p0400' + '{:02x}'.format(int(power)) + '20' + '{:02x}'.format(int(power))
        print ('forward ' + str(power) + ' ' + cmd)
        self.out.write(cmd.encode('utf-8'))

    @pyqtSlot(int)
    def backward(self, power):
        power = (power * 255) / 100
        cmd = '0p0800' + '{:02x}'.format(int(power)) + '20' + '{:02x}'.format(int(power))
        print ('backward ' + str(power) + ' ' + cmd)
        self.out.write(cmd.encode('utf-8'))


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
