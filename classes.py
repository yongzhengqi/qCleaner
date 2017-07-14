from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from functions import *
import os


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("qCleaner")
        self.setWindowIcon(QIcon("icon.png"))

        self.InitWidget()

        self.setLayout(self.MainGrid)
        self.show()

    def InitWidget(self):
        PathLabel = QLabel("操作目录")

        PathEdit = QLineEdit()

        BrowseButton = QPushButton("浏览")
        BrowseButton.clicked.connect(lambda: BrowseDialog(PathEdit))

        ProcessButton = QPushButton("清理")
        ProcessButton.clicked.connect(lambda: MainProcessGuide(PathEdit.text()))

        self.MainGrid = QGridLayout()
        self.MainGrid.setSpacing(10)

        self.MainGrid.addWidget(PathLabel, 1, 1)
        self.MainGrid.addWidget(PathEdit, 1, 2)
        self.MainGrid.addWidget(BrowseButton, 1, 3)
        self.MainGrid.addWidget(ProcessButton, 2, 1, 1, 3)


class ProcessModule(QDialog):
    def __init__(self, path):
        super().__init__()

        self.setWindowTitle("正在清理")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(300, 200)

        self.PathCount = self.FileCount = self.SpaceCount = 0
        self.UpdateCount = self.ForcedTerminated = 0

        self.PathCountStatus = QLabel()
        self.FileCountStatus = QLabel()
        self.SpaceCountStatus = QLabel()
        self.CurrentPathStatus = QLabel()

        self.ExitButton = QPushButton("取消")
        self.ExitButton.clicked.connect(self.ForcedTermination)

        GridLayout = QGridLayout()
        GridLayout.addWidget(self.CurrentPathStatus, 1, 1)
        GridLayout.addWidget(self.PathCountStatus, 2, 1)
        GridLayout.addWidget(self.FileCountStatus, 3, 1)
        GridLayout.addWidget(self.SpaceCountStatus, 4, 1)
        GridLayout.addWidget(self.ExitButton, 5, 1)
        self.setLayout(GridLayout)

        import threading
        process = threading.Thread(target=self.ProcessGuide, args=(path,))
        process.start()

    def ForcedTermination(self):
        self.ForcedTerminated = 1

    def ProcessGuide(self, path):
        self.process(path, 500)

        self.UpdateData("")
        self.ExitButton.setText("确定")
        self.ExitButton.clicked.disconnect(self.ForcedTermination)
        self.ExitButton.clicked.connect(self.close)

        if self.ForcedTerminated:
            self.setWindowTitle("已取消")
        else:
            self.setWindowTitle("清理完成")

    def UpdateData(self, CurrentPath):
        self.CurrentPathStatus.setText("当前目录：%s" % CurrentPath)
        self.PathCountStatus.setText("已遍历%d个文件夹" % self.PathCount)
        self.FileCountStatus.setText("已删除%d个.exe文件" % self.FileCount)
        self.SpaceCountStatus.setText("已释放出%dMB的空间" % (self.SpaceCount / 1024 / 1024))

    def process(self, path, UpdateCountBase):
        if self.ForcedTerminated:
            return

        self.PathCount += 1

        try:
            FileList = os.listdir(path)
        except:
            return

        for file in FileList:
            self.UpdateCount -= 1
            if self.UpdateCount <= 0:
                self.UpdateData(path)
                self.UpdateCount = UpdateCountBase

            AbsolutePath = path + os.sep + file
            if os.path.isdir(AbsolutePath):
                self.process(AbsolutePath, UpdateCountBase)
            elif os.path.splitext(file)[1] == ".cpp":
                ExecutableFile = os.path.splitext(file)[0] + ".exe"
                if (ExecutableFile in FileList):
                    self.SpaceCount += os.path.getsize(path + os.sep + ExecutableFile)
                    self.FileCount += 1
                    self.UpdateData(path)

                    os.remove(path + os.sep + ExecutableFile)
