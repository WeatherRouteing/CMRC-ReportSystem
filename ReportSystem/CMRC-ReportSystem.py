import datetime

import pymysql
from PyQt5.QtGui import QColor

from ReportSystem.LogView import LogViewWindow
from ReportSystem.UiCode.Ui_MainWindow import Ui_MainWindow


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMessageBox, QInputDialog, QLineEdit, QMenu, QTextEdit, QLabel, QTableWidget, \
    QTableWidgetItem, QApplication, QColorDialog, QPushButton
from PyQt5.QtCore import QObject, Qt, QPoint, pyqtSignal
import sys

shiptypedict = {
    0: "service = 1 and running = 1 and inport = 0",
    1: "service = 0 and running = 1 and inport = 1",
    2: "service = 0 and running = 0 and inport = 0",
    3: "estreport = 1",
    4: "service = 0 and running = 0 and inport = 1",
    5: "service = 1 and running = 1 and inport = 0"
}
SortUporDown = True


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, SortUporDown):
        QtWidgets.QMainWindow.__init__(self)
        self.SortUporDown = SortUporDown
        self.setupUi(self)
        # 设置当前日期
        date = datetime.datetime.utcnow()
        self.dateEdit.setDate(date)
        # 先绑定几个复选框的函数
        self.checkBox_service_inline.stateChanged.connect(self.updateShipList)  # 0
        self.checkBox_service_inport.stateChanged.connect(self.updateShipList)  # 1
        self.checkBox_service_wait.stateChanged.connect(self.updateShipList)  # 2
        self.checkBox_finish_est.stateChanged.connect(self.updateShipList)  # 3
        self.checkBox_finish_voy.stateChanged.connect(self.updateShipList)  # 4
        self.checkBox_drop.stateChanged.connect(self.updateShipList)  # 5
        # 调整时间表格改变
        self.dateEdit.dateChanged.connect(self.updateShipList)
        # 连接表头排序函数
        self.tableWidget_main_window.horizontalHeader().sectionClicked.connect(self.HorSectionClicked)
        # 设置表格右键函数
        self.tableWidget_main_window.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键产生子菜单
        self.tableWidget_main_window.customContextMenuRequested.connect(self.generateMenu)  # 右键菜单



        #更新和删除值班表
        self.pushButton_update.clicked.connect(self.updatedutyform)
        self.pushButton_del.clicked.connect(self.deldutyform)


        # 设置发报标记的颜色
        self.tableWidget_main_window.itemDoubleClicked.connect(self.SetBackgroundColor)
        # 设置表头日期
        date = self.dateEdit.date().toString(Qt.ISODate)
        dateTomorrow = datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days=1)
        dateToday = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m-%d')
        dateTomorrow = dateTomorrow.strftime('%m-%d')
        self.tableWidget_main_window.setHorizontalHeaderItem(0, QTableWidgetItem(str(dateTomorrow)))
        self.tableWidget_main_window.setHorizontalHeaderItem(1, QTableWidgetItem(str(dateToday)))

    def deldutyform(self):
        date = self.dateEdit.date().toPyDate()
        try:
            db_connect = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                         db='cmrcreportsystemdb',
                                         charset='utf8')
            cursor = db_connect.cursor()
            sql = f"delete from dutyform where dutydate = '{date}'"
            cursor.execute(sql)
            db_connect.commit()
            db_connect.close()
        except Exception as e:
            QMessageBox.warning(self, '失败',  date.strftime('%Y-%m-%d') + '号值班表删除失败：' + str(e), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            QMessageBox.information(self, '成功', date.strftime('%Y-%m-%d') + ' 号值班表删除成功',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def updatedutyform(self):
        date = self.dateEdit.date().toPyDate()
        date_index = date - datetime.timedelta(days=1)
        try:
            db_connect = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                         db='cmrcreportsystemdb',
                                         charset='utf8')
            cursor = db_connect.cursor()
            sql = f"select * from dutyform where dutydate = '{date_index}'"
            cursor.execute(sql)
            dutyinf = cursor.fetchall()
            if dutyinf:
                for i in range(len(dutyinf)):
                    voy = dutyinf[i][2]
                    forecast_Date_today = dutyinf[i][3]
                    forecast_Date_tomorrow = dutyinf[i][4]
                    sql = f"select * from dutyform where dutydate = '{date}' and voy = {voy}"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        sql = f"update dutyform set forecast_Date_tomorrow = '{forecast_Date_tomorrow}'," \
                              f" forecast_Date_today = '{forecast_Date_today}' where dutydate = '{date}' and voy = {voy}"
                        cursor.execute(sql)
                        db_connect.commit()
                    else:
                        sql = f"INSERT into dutyform (dutydate,voy,forecast_Date_tomorrow,forecast_Date_today) values" \
                              f" ('{date}',{voy},'{forecast_Date_tomorrow}','{forecast_Date_today}')"
                        cursor.execute(sql)
                        db_connect.commit()
            db_connect.close()
        except Exception as e:
            QMessageBox.warning(self, '失败', '更新失败：'+ str(e), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            if dutyinf:
                QMessageBox.information(self, '成功', date.strftime('%Y-%m-%d')+' 号值班表更新成功', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                QMessageBox.information(self, '提示', '未查询到' + date_index.strftime('%Y-%m-%d') + '号值班表',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    # 更新背景色和打开各类报文发报
    def SetBackgroundColor(self, index):
        try:
            row = index.row()
            col = index.column()
            if col == 0 or col == 1:
                color = QColorDialog.getColor()
                if color.isValid():
                    self.tableWidget_main_window.item(row, col).setBackground(QColor(color.name()))
                    db_connect = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                                 db='cmrcreportsystemdb',
                                                 charset='utf8')
                    cursor = db_connect.cursor()
                    date = self.dateEdit.date().toPyDate()
                    sql = f"select * from dutyform where dutydate = '{date}' and voy = {int(self.tableWidget_main_window.item(row, 3).text())}"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        if col == 0:
                            sql = f"UPDATE dutyform set forecast_Date_tomorrow = '{color.name()}' where " \
                                  f"dutydate = '{date}' and voy = {self.tableWidget_main_window.item(row, 3).text()}"
                            cursor.execute(sql)
                            db_connect.commit()
                        else:
                            sql = f"UPDATE dutyform set forecast_Date_today = '{color.name()}' where " \
                                  f"dutydate = '{date}' and voy = {self.tableWidget_main_window.item(row, 3).text()}"
                            cursor.execute(sql)
                            db_connect.commit()
                    else:
                        if col == 0:
                            sql = f"INSERT into dutyform (dutydate,voy,forecast_Date_tomorrow) values" \
                                  f" ('{date}',{self.tableWidget_main_window.item(row, 3).text()},'{color.name()}')"
                            cursor.execute(sql)
                            db_connect.commit()
                        else:
                            sql = f"INSERT into dutyform (dutydate,voy,forecast_Date_today) values" \
                                  f" ('{date}',{self.tableWidget_main_window.item(row, 3).text()},'{color.name()}')"
                            cursor.execute(sql)
                            db_connect.commit()

                    sql = f"select * from dutyform where dutydate = '{date}' and voy = {self.tableWidget_main_window.item(row, 3).text()}"
                    cursor.execute(sql)
                    dutyinf = cursor.fetchall()
                    if dutyinf:
                        if (dutyinf[0][3] == '' or dutyinf[0][3] == '#ffffff') and (
                                dutyinf[0][4] == '' or dutyinf[0][4] == '#ffffff'):
                            self.tableWidget_main_window.item(row, 5).\
                                setBackground(QColor('#cccccc'))
                        else:
                            self.tableWidget_main_window.item(row, 5). \
                                setBackground(QColor('#ffffff'))
                    db_connect.close()
            else:
                if col == 5:
                    print('打开预报')
                else:
                    if col == 6:
                        print('打开日报')
                    else:
                        if col == 2 or col == 3 or col == 4:
                            print('qita')
                        else:
                            print('text')
        except Exception as e:
            QMessageBox.warning(self, '失败', '失败：' + str(e), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    # 表头点击排序函数
    def HorSectionClicked(self, index):
        if self.SortUporDown:
            self.tableWidget_main_window.sortByColumn(index, Qt.AscendingOrder)
            self.SortUporDown = False
        else:
            self.tableWidget_main_window.sortByColumn(index, Qt.DescendingOrder)
            self.SortUporDown = True

    def generateMenu(self, pos):
        row_num = -1
        for i in self.tableWidget_main_window.selectionModel().selection().indexes():
            row_num = i.row()
        menu = QMenu()
        item1 = menu.addAction(u"发送报文")
        item2 = menu.addAction(u"值班日志")
        action = menu.exec_(self.tableWidget_main_window.mapToGlobal(pos))
        if action == item1:
            print('2')
            # self.set_ship_parameter_window = SendWindow()
            # self.set_ship_parameter_window.show()
        else:
            if action == item2:
                self.LogView = LogViewWindow(self.tableWidget_main_window.item(row_num, 2).text(),
                                             self.tableWidget_main_window.item(row_num, 3).text())
                self.LogView.show()

    # 服务中复选框函数
    def updateShipList(self):
        try:
            # 设置表头日期
            date = self.dateEdit.date().toString(Qt.ISODate)
            dateTomorrow = datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days=1)
            dateToday = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m-%d')
            dateTomorrow = dateTomorrow.strftime('%m-%d')
            self.tableWidget_main_window.setHorizontalHeaderItem(0, QTableWidgetItem(str(dateTomorrow)))
            self.tableWidget_main_window.setHorizontalHeaderItem(1, QTableWidgetItem(str(dateToday)))
            # 获取所有勾选中的船舶服务状态
            self.tableWidget_main_window.setRowCount(0)
            shipListState = []
            if self.checkBox_service_inline.checkState() == 2:
                shipListState.append(0)
            if self.checkBox_service_inport.checkState() == 2:
                shipListState.append(1)
            if self.checkBox_service_wait.checkState() == 2:
                shipListState.append(2)
            if self.checkBox_finish_est.checkState() == 2:
                shipListState.append(3)
            if self.checkBox_finish_voy.checkState() == 2:
                shipListState.append(4)
            if self.checkBox_drop.checkState() == 2:
                shipListState.append(5)
            """
            开始更新界面，每点击一次复选框，更新一次界面
            """
            date = self.dateEdit.date().toPyDate()
            if shipListState:
                db_connect = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                             db='cmrcreportsystemdb',
                                             charset='utf8')
                cursor = db_connect.cursor()
                for shiptype in shipListState:
                    sql = f"select * from reportsystemcontract where {shiptypedict[shiptype]}"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for i in range(len(result)):
                        num = self.tableWidget_main_window.rowCount()
                        self.tableWidget_main_window.setRowCount(num + 1)
                        self.tableWidget_main_window.setRowHeight(num, 80)
                        self.tableWidget_main_window.setItem(num, 0, QTableWidgetItem(''))
                        self.tableWidget_main_window.setItem(num, 1, QTableWidgetItem(''))
                        self.tableWidget_main_window.setItem(num, 2, QTableWidgetItem(result[i][3]))
                        self.tableWidget_main_window.setItem(num, 3, QTableWidgetItem(str(result[i][4])))
                        self.tableWidget_main_window.setItem(num, 5, QTableWidgetItem(' '))
                        self.tableWidget_main_window.setItem(num, 6, QTableWidgetItem(' '))
                        # 判断日报是否需要发送
                        sql = f"select * from shipparm where voy = {result[i][4]}"
                        cursor.execute(sql)
                        dayilyreport = cursor.fetchall()
                        if dayilyreport:
                            if dayilyreport[0][1] == '不发送':
                                self.tableWidget_main_window.item(num, 6).setBackground(QColor('#cccccc'))
                        # 获取时次
                        sql = f"select * from sendhistory where reporttype = 0 and voy = {result[i][4]}"
                        cursor.execute(sql)
                        timeindex = cursor.fetchall()
                        if timeindex:
                            timeindex = timeindex[-1][-1][-2:]
                        else:
                            timeindex = ''
                        self.tableWidget_main_window.setItem(num, 4, QTableWidgetItem(str(timeindex)))
                        # 先从dutyform数据库中查找该航次在该日期的信息！
                        sql = f"select * from dutyform where dutydate = '{date}' and voy = {result[i][4]}"
                        cursor.execute(sql)
                        dutyinf = cursor.fetchall()
                        if dutyinf:
                            if dutyinf[0][3]:
                                self.tableWidget_main_window.item(num, 0).setBackground(QColor(dutyinf[0][3]))
                            if dutyinf[0][4]:
                                self.tableWidget_main_window.item(num, 1).setBackground(QColor(dutyinf[0][4]))
                            if dutyinf[0][5]:
                                self.tableWidget_main_window.setItem(num, 5, QTableWidgetItem(str(dutyinf[0][5])))
                            if dutyinf[0][6]:
                                self.tableWidget_main_window.setItem(num, 6, QTableWidgetItem(str(dutyinf[0][6])))
                            if (dutyinf[0][3] == '' or dutyinf[0][3] == '#ffffff')  and (dutyinf[0][4] == '' or dutyinf[0][4] == '#ffffff'):
                                self.tableWidget_main_window.item(num, 5).setBackground(QColor('#cccccc'))
                        else:
                            self.tableWidget_main_window.item(num, 5).setBackground(QColor('#cccccc'))

                        Text = QTextEdit()
                        Text.setReadOnly(True)
                        # 获取该航次的需要关注的值班日志
                        sql = f"select * from dutylog where voy = {result[i][4]}"
                        cursor.execute(sql)
                        dutylog = cursor.fetchall()
                        if dutylog:
                            dutylog = list(dutylog)
                            dutylog.reverse()
                            for i in range(len(dutylog)):
                                Text.append(dutylog[i][3].strftime('%Y-%m-%d %H:%M') + ': ' + dutylog[i][4])
                        self.tableWidget_main_window.setCellWidget(num, 7, Text)
                        pushbuttoneditlog = QPushButton('编辑')
                        self.tableWidget_main_window.setCellWidget(num,8,pushbuttoneditlog)
                        pushbuttoneditlog.clicked.connect(self.openlogview)
        except Exception as e:
            QMessageBox.warning(self, '失败', '失败：' + str(e), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def openlogview(self):
        senderobj = self.sender()
        x = senderobj.frameGeometry().x()
        y = senderobj.frameGeometry().y()
        index = self.tableWidget_main_window.indexAt(QPoint(x, y))
        row = index.row()
        shipname = self.tableWidget_main_window.item(row,2).text()
        voy = self.tableWidget_main_window.item(row,3).text()
        self.LogView = LogViewWindow(shipname,voy)
        self.LogView.show()



class TextEvent():
    def up(self):
        print('1')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(SortUporDown)
    window.show()
    sys.exit(app.exec_())
