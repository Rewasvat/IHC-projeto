import sys
from PyQt5.QtWidgets import QApplication

from dpcs.manager import SymbolManager

app = QApplication(sys.argv)

screen = SymbolManager()
screen.show()

sys.exit(app.exec_())
