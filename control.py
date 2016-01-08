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
    def left(self):
        print ('left')
        cmd = '0p0100000000'
        self.out.write(cmd.encode('utf-8'))

    @pyqtSlot()
    def right(self):
        print ('right')
        cmd = '0p0200000000'
        self.out.write(cmd.encode('utf-8'))

    @pyqtSlot()
    def forward(self):
        print ('forward')
        cmd = '0p04001f0000'
        self.out.write(cmd.encode('utf-8'))

    @pyqtSlot()
    def backward(self):
        print ('backward')
        cmd = '0p0800ff0000'
        self.out.write(cmd.encode('utf-8'))


if __name__ == "__main__":
    port = "/dev/rfcomm0"
    ctrl = Control(port)
    app = QApplication(sys.argv)
    view = QQuickView()
    view.setSource(QUrl('QtUi/main.qml'))
    context = view.rootContext()
    context.setContextProperty("control", ctrl)

    view.show()
    app.exec_()
    sys.exit()
