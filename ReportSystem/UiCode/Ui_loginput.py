# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\working\CMRC-ReportSystem\ReportSystem\UiCode\loginput.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LogInput(object):
    def setupUi(self, LogInput):
        LogInput.setObjectName("LogInput")
        LogInput.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(LogInput)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(LogInput)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(LogInput)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(LogInput)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(LogInput)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(LogInput)
        QtCore.QMetaObject.connectSlotsByName(LogInput)

    def retranslateUi(self, LogInput):
        _translate = QtCore.QCoreApplication.translate
        LogInput.setWindowTitle(_translate("LogInput", "Dialog"))
        self.pushButton.setText(_translate("LogInput", "天气"))
        self.pushButton_2.setText(_translate("LogInput", "航线"))
        self.pushButton_3.setText(_translate("LogInput", "其他"))
