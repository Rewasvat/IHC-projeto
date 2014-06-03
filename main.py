#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

from dpcs.manager import SymbolManager

from dpcs.speaker import Speaker
spTeste = Speaker()
spTeste.speak("deleteMe", "Testando 1 2 3")


app = QGuiApplication(sys.argv)

qmlRegisterType(Speaker, 'Speaker', 1, 0, 'Speaker')

view = QQuickView()
view.engine().quit.connect(app.quit)

view.setSource(QUrl('teste.qml'))
view.show()

sys.exit(app.exec_())
