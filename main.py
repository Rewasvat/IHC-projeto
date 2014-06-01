#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from dpcs.manager import SymbolManager

from dpcs.speaker import Speaker
spTeste = Speaker()
spTeste.speak("deleteMe", "Testando 1 2 3")

app = QApplication(sys.argv)

screen = SymbolManager()
screen.show()

sys.exit(app.exec_())
