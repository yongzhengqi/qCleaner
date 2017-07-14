import os
import sys
from PyQt5.QtWidgets import *


def MainProcessGuide(path):
    if not os.path.exists(path):
        RaiseWarning("路径错误")
        return

    if not GetConfirm("数据无价请先做好备份工作"):
        RaiseMessage("清理已终止")
        return

    from classes import ProcessModule

    MainProcess = ProcessModule(path)
    MainProcess.exec_()


def BrowseDialog(PathEdit):
    FilePath = QFileDialog.getExistingDirectory()
    FilePath = os.path.abspath(FilePath)
    PathEdit.setText(FilePath)


def RaiseWarning(info):
    MessageBox = QMessageBox()
    MessageBox.setIcon(QMessageBox.Warning)
    MessageBox.setText(info)
    MessageBox.setWindowTitle("Warning")
    MessageBox.exec_()


def RaiseMessage(info):
    MessageBox = QMessageBox()
    MessageBox.setIcon(QMessageBox.Information)
    MessageBox.setText(info)
    MessageBox.setWindowTitle("Message")
    MessageBox.exec_()


def GetConfirm(info):
    MessageBox = QMessageBox()
    MessageBox.setIcon(QMessageBox.Question)
    MessageBox.setText(info)
    MessageBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    MessageBox.setWindowTitle("Please Confirm")
    return MessageBox.exec_() == QMessageBox.Ok
