# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\vscode\VS-Code-Python\CMRC-ReportSystem\ReportSystem\UiCode\SendThreeDays.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SendThreeDays(object):
    def setupUi(self, SendThreeDays):
        SendThreeDays.setObjectName("SendThreeDays")
        SendThreeDays.resize(895, 809)
        self.centralwidget = QtWidgets.QWidget(SendThreeDays)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.textEdit_send = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_send.setObjectName("textEdit_send")
        self.verticalLayout_4.addWidget(self.textEdit_send)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.textEdit_sendcc = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_sendcc.setObjectName("textEdit_sendcc")
        self.verticalLayout_5.addWidget(self.textEdit_sendcc)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.horizontalLayout_4.setStretch(0, 10)
        self.horizontalLayout_4.setStretch(1, 10)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout_2.setStretch(0, 7)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.horizontalLayout_3.setStretch(0, 7)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 10)
        self.verticalLayout_6.addLayout(self.verticalLayout_3)
        SendThreeDays.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SendThreeDays)
        self.statusbar.setObjectName("statusbar")
        SendThreeDays.setStatusBar(self.statusbar)

        self.retranslateUi(SendThreeDays)
        QtCore.QMetaObject.connectSlotsByName(SendThreeDays)

    def retranslateUi(self, SendThreeDays):
        _translate = QtCore.QCoreApplication.translate
        SendThreeDays.setWindowTitle(_translate("SendThreeDays", "MainWindow"))
        self.label.setText(_translate("SendThreeDays", "发送邮箱："))
        self.label_4.setText(_translate("SendThreeDays", "转发邮箱"))
        self.pushButton.setText(_translate("SendThreeDays", "打开"))
        self.pushButton_2.setText(_translate("SendThreeDays", "发送"))
        self.label_2.setText(_translate("SendThreeDays", "三天预报发送记录："))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SendThreeDays", "起报时次"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SendThreeDays", "发送时间"))
        self.label_3.setText(_translate("SendThreeDays", "邮件正文："))