import sys
from PyQt5.QtWidgets import *
from classes import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainProg = Main()
    sys.exit(app.exec_())
