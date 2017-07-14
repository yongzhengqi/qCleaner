import sys
from cx_Freeze import setup, Executable


setup(name = "qCleaner" ,
      version = "1.0" ,
      description = "qCleaner" ,
      options = {},
      executables = [Executable("qCleaner.py", base = "Win32GUI", icon = "icon.ico")])