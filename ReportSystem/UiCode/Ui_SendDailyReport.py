# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\vscode\VS-Code-Python\CMRC-ReportSystem\ReportSystem\UiCode\SendDailyReport.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SendDailyReport(object):
    def setupUi(self, SendDailyReport):
        SendDailyReport.setObjectName("SendDailyReport")
        SendDailyReport.resize(874, 794)
        self.centralwidget = QtWidgets.QWidget(SendDailyReport)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textEdit_send = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_send.setObjectName("textEdit_send")
        self.verticalLayout.addWidget(self.textEdit_send)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.textEdit_send_cc = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_send_cc.setObjectName("textEdit_send_cc")
        self.verticalLayout_2.addWidget(self.textEdit_send_cc)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.setStretch(0, 10)
        self.horizontalLayout_2.setStretch(1, 10)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_open = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_open.setObjectName("pushButton_open")
        self.horizontalLayout.addWidget(self.pushButton_open)
        self.pushButton_gen = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_gen.setObjectName("pushButton_gen")
        self.horizontalLayout.addWidget(self.pushButton_gen)
        self.horizontalLayout.setStretch(0, 6)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 5)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        SendDailyReport.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SendDailyReport)
        self.statusbar.setObjectName("statusbar")
        SendDailyReport.setStatusBar(self.statusbar)

        self.retranslateUi(SendDailyReport)
        QtCore.QMetaObject.connectSlotsByName(SendDailyReport)

    def retranslateUi(self, SendDailyReport):
        _translate = QtCore.QCoreApplication.translate
        SendDailyReport.setWindowTitle(_translate("SendDailyReport", "MainWindow"))
        self.label.setText(_translate("SendDailyReport", "???????????????"))
        self.label_2.setText(_translate("SendDailyReport", "????????????"))
        self.pushButton_open.setText(_translate("SendDailyReport", "??????"))
        self.pushButton_gen.setText(_translate("SendDailyReport", "????????????"))
