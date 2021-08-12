import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QTextEdit, QMenu
import time
from ReportSystem.UiCode.Ui_LogView import Ui_LogView
from ReportSystem.UiCode.Ui_loginput import Ui_LogInput


class LogViewWindow(QtWidgets.QMainWindow, Ui_LogView):
    def __init__(self, shipname, voy):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        # 设置表格右键函数
        self.tableWidget_un.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键产生子菜单
        self.tableWidget_un.customContextMenuRequested.connect(lambda :self.generateMenuUn(shipname))  # 右键菜单
        # self.tableWidget_done.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键产生子菜单
        # self.tableWidget_done.customContextMenuRequested.connect(self.generateMenuDone)  # 右键菜单
        db_connect = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                     db='cmrcreportsystemdb',
                                     charset='utf8')
        cursor = db_connect.cursor()
        # 查找待解决日志
        sql = f"select * from dutylog where voy = {int(voy)} and mark = 0"
        cursor.execute(sql)
        dutylog = cursor.fetchall()
        if dutylog:
            self.tableWidget_done.setRowCount(len(dutylog))
            dutylog = list(dutylog)
            dutylog.reverse()
            for i in range(len(dutylog)):
                self.tableWidget_un.setItem(i, 0, QTableWidgetItem(dutylog[i][3].strftime('%Y-%m-%d %H:%M:%S')))
                self.tableWidget_un.setRowHeight(i, 60)
                Text = QTextEdit()
                Text.setReadOnly(True)
                Text.append(dutylog[i][4])
                self.tableWidget_un.setCellWidget(i, 1, Text)
                self.tableWidget_un.setItem(i,2,QTableWidgetItem(dutylog[i][-1]))
        sql = f"select * from dutylog where voy = {int(voy)} and mark = 1"
        cursor.execute(sql)
        dutylog = cursor.fetchall()
        if dutylog:
            self.tableWidget_done.setRowCount(len(dutylog))
            dutylog = list(dutylog)
            dutylog.reverse()
            for i in range(len(dutylog)):
                self.tableWidget_done.setItem(i, 0, QTableWidgetItem(dutylog[i][3].strftime('%Y-%m-%d %H:%M:%S')))
                self.tableWidget_done.setRowHeight(i, 60)
                Text = QTextEdit()
                Text.setReadOnly(True)
                Text.append(dutylog[i][4])
                self.tableWidget_done.setCellWidget(i, 1, Text)
                self.tableWidget_done.setItem(i, 2, QTableWidgetItem(dutylog[i][-1]))
        # 获取该船舶所有航次的值班日志
        sql = f"select voy from dutylog where shipname = '{shipname}' group by voy"
        cursor.execute(sql)
        dutylog = cursor.fetchall()
        if dutylog:
            for i in range(len(dutylog)):
                self.comboBox.addItem(str(dutylog[i][0]))
        else:
            self.comboBox.addItem(str(voy))
        self.comboBox.setCurrentText(str(voy))
        db_connect.close()
        # 当选择栏改变，则连接函数
        self.comboBox.currentTextChanged.connect(lambda: self.getdutylog(self.comboBox.currentText()))

    def getdutylog(self, voy):
        self.tableWidget_un.clearContents()
        self.tableWidget_done.clearContents()
        db_connect = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                     db='cmrcreportsystemdb',
                                     charset='utf8')
        cursor = db_connect.cursor()
        # 查找待解决日志
        sql = f"select * from dutylog where voy = {int(voy)} and mark = 0"
        cursor.execute(sql)
        dutylog = cursor.fetchall()
        self.tableWidget_un.setRowCount(len(dutylog))
        if dutylog:
            dutylog = list(dutylog)
            dutylog.reverse()
            for i in range(len(dutylog)):
                self.tableWidget_un.setItem(i, 0, QTableWidgetItem(dutylog[i][3].strftime('%Y-%m-%d %H:%M:%S')))
                self.tableWidget_un.setRowHeight(i,60)
                Text = QTextEdit()
                Text.setReadOnly(True)
                Text.append(dutylog[i][4])
                self.tableWidget_un.setCellWidget(i, 1, Text)
                self.tableWidget_un.setItem(i, 2, QTableWidgetItem(dutylog[i][-1]))
        sql = f"select * from dutylog where voy = {int(voy)} and mark = 1"
        cursor.execute(sql)
        dutylog = cursor.fetchall()
        self.tableWidget_done.setRowCount(len(dutylog))
        if dutylog:
            dutylog = list(dutylog)
            dutylog.reverse()
            for i in range(len(dutylog)):
                self.tableWidget_done.setItem(i, 0, QTableWidgetItem(dutylog[i][3].strftime('%Y-%m-%d %H:%M:%S')))
                self.tableWidget_done.setRowHeight(i, 60)
                Text = QTextEdit()
                Text.setReadOnly(True)
                Text.append(dutylog[i][4])
                self.tableWidget_done.setCellWidget(i, 1, Text)
                self.tableWidget_done.setItem(i, 2, QTableWidgetItem(dutylog[i][-1]))
        db_connect.close()

    def generateMenuUn(self,shipname,pos):
        row_num = -1
        for i in self.tableWidget_un.selectionModel().selection().indexes():
            row_num = i.row()
        menu = QMenu()
        item1 = menu.addAction(u"添加日志")
        item2 = menu.addAction(u"修改日志")
        item3 = menu.addAction(u"移动至已解决")
        item4 = menu.addAction(u"删除日志")
        action = menu.exec_(self.tableWidget_un.mapToGlobal(pos))
        if action == item1:
            self.TextInput = LogInput('添加日志',int(self.comboBox.currentText(),shipname))
            self.TextInput.show()
        else:
            if action == item2:
                date = self.tableWidget_un.item(row_num,0).text()
                self.TextInput = LogInput(date,int(self.comboBox.currentText()))
                self.TextInput.show()
            else:
                db_connect = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                             db='cmrcreportsystemdb',
                                             charset='utf8')
                cursor = db_connect.cursor()
                # 查找待解决日志
                sql = f"set mark = 1 from dutylog where voy = {int(self.comboBox.currentText())} "
                cursor.execute(sql)


class LogInput(QtWidgets.QDialog, Ui_LogInput):
    def __init__(self,title,voy,shipname):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(title)
        if self.windowTitle() == '添加日志':
            self.pushButton.clicked.connect(lambda :self.insertlog(self.pushButton.text()),voy,shipname)
            self.pushButton_2.clicked.connect(lambda: self.insertlog(self.pushButton_2.text()),voy,shipname)
            self.pushButton_3.clicked.connect(lambda: self.insertlog(self.pushButton_3.text()),voy,shipname)
        else:
            db_connect = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                         db='cmrcreportsystemdb',
                                         charset='utf8')
            cursor = db_connect.cursor()
            # 查找待解决日志
            sql = f"select * from dutylog where voy = {int(voy)} and date = '{self.windowTitle()}'"
            cursor.execute(sql)
            dutylog = cursor.fetchall()
            print(dutylog)
            self.pushButton.setText('确认修改')
        # self.pushButton.clicked.connect(self.updatelog())

    def insertlog(self,text,voy,shipname):
        db_connect = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                     db='cmrcreportsystemdb',
                                     charset='utf8')
        cursor = db_connect.cursor()
        inserttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if self.textEdit.toPlainText():
            sql = f"insert into dutylog (shipname,voy,logdate,log,mark,logtype) values ({shipname},{voy},{inserttime})"
            cursor.execute(sql)
            db_connect.commit()
            self.textEdit.append('添加成功')
    def updatelog(self):
        log = self.textEdit.toPlainText()
        if self.windowTitle() == '添加日志':
            print('1')