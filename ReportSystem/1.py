import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QTextEdit
from PySide2.QtCore import SIGNAL


def text_change():
    print ("change ok")
def text_click(event): # < - NOTE: event object is passed.
    print ("clicked ok ")

app = QApplication(sys.argv)
textEdit = QTextEdit()
textEdit.setGeometry(QtCore.QRect(30, 20, 351, 51))
textEdit.setObjectName("textEdit")
textEdit.mousePressEvent = text_click
QtCore.QObject.connect(textEdit, SIGNAL("textChanged()"), text_change)
textEdit.show()
sys.exit(app.exec_())