#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

from dpcs.speaker import Speaker
from dpcs.qmlmodel import Database, Category, Symbol

app = QGuiApplication(sys.argv)

qmlRegisterType(Speaker, 'DPCS', 1, 0, 'Speaker')
qmlRegisterType(Database, 'DPCS', 1, 0, 'Database')
qmlRegisterType(Category, 'DPCS', 1, 0, 'Category')
qmlRegisterType(Symbol, 'DPCS', 1, 0, 'Symbol')

view = QQuickView()
view.engine().quit.connect(app.quit)

view.setSource(QUrl('teste.qml'))
view.show()

sys.exit(app.exec_())
