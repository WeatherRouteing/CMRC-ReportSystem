# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\vscode\VS-Code-Python\CMRC-ReportSystem\ReportSystem\UiCode\SendView.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SendView(object):
    def setupUi(self, SendView):
        SendView.setObjectName("SendView")
        SendView.resize(588, 467)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(SendView)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(10)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_6 = QtWidgets.QLabel(SendView)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_10.addWidget(self.label_6)
        self.comboBox = QtWidgets.QComboBox(SendView)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_10.addWidget(self.comboBox)
        self.label_7 = QtWidgets.QLabel(SendView)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_10.addWidget(self.label_7)
        self.label = QtWidgets.QLabel(SendView)
        self.label.setObjectName("label")
        self.horizontalLayout_10.addWidget(self.label)
        self.verticalLayout_6.addLayout(self.horizontalLayout_10)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableWidget = QtWidgets.QTableWidget(SendView)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.verticalLayout_3.addWidget(self.tableWidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(SendView)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.textEdit = QtWidgets.QTextEdit(SendView)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_6.addLayout(self.verticalLayout_3)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton_daily_report = QtWidgets.QPushButton(SendView)
        self.pushButton_daily_report.setObjectName("pushButton_daily_report")
        self.verticalLayout_4.addWidget(self.pushButton_daily_report)
        self.pushButton_three_days = QtWidgets.QPushButton(SendView)
        self.pushButton_three_days.setObjectName("pushButton_three_days")
        self.verticalLayout_4.addWidget(self.pushButton_three_days)
        self.pushButton_five_days = QtWidgets.QPushButton(SendView)
        self.pushButton_five_days.setObjectName("pushButton_five_days")
        self.verticalLayout_4.addWidget(self.pushButton_five_days)
        self.pushButton_est = QtWidgets.QPushButton(SendView)
        self.pushButton_est.setObjectName("pushButton_est")
        self.verticalLayout_4.addWidget(self.pushButton_est)
        self.pushButton_other = QtWidgets.QPushButton(SendView)
        self.pushButton_other.setObjectName("pushButton_other")
        self.verticalLayout_4.addWidget(self.pushButton_other)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)

        self.retranslateUi(SendView)
        QtCore.QMetaObject.connectSlotsByName(SendView)

    def retranslateUi(self, SendView):
        _translate = QtCore.QCoreApplication.translate
        SendView.setWindowTitle(_translate("SendView", "Dialog"))
        self.label_6.setText(_translate("SendView", "日报："))
        self.comboBox.setItemText(0, _translate("SendView", "发送"))
        self.comboBox.setItemText(1, _translate("SendView", "不发送"))
        self.label_7.setText(_translate("SendView", "数据包："))
        self.label.setText(_translate("SendView", "发送"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("SendView", "数据包"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("SendView", "三天预报"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("SendView", "五天预报"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("SendView", "航次评估报"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SendView", "时次"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SendView", "生成时间"))
        self.label_5.setText(_translate("SendView", "值班日志："))
        self.pushButton_daily_report.setText(_translate("SendView", "日报"))
        self.pushButton_three_days.setText(_translate("SendView", "三天预报"))
        self.pushButton_five_days.setText(_translate("SendView", "五天预报"))
        self.pushButton_est.setText(_translate("SendView", "航次评估报"))
        self.pushButton_other.setText(_translate("SendView", "其他报文"))
