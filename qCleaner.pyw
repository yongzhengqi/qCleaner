import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from classes import *

if __name__ == "__main__":
    app = QApplication(sys.argv)

    QssFile = QFile('StyleSheets.qss')
    QssFile.open(QFile.ReadOnly)
    StyleSheet = QssFile.readAll()
    app.setStyleSheet(QTextStream(StyleSheet).readAll())

    MainProg = Main()

    sys.exit(app.exec_())
