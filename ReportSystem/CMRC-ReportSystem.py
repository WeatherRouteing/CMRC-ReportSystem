import datetime

import pymysql
from PyQt5.QtGui import QBrush, QColor

from ReadFileFun.ReadNewEstimateFile import read_estimate_report
from ReportSystem.UiCode.Ui_LogView import Ui_LogView
from ReportSystem.UiCode.Ui_MainWindow import Ui_MainWindow
from ReportSystem.UiCode.Ui_loginput import Ui_LogInput
from ReportSystem.UiCode.Ui_sendmain import Ui_SendWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMessageBox, QInputDialog, QLineEdit, QMenu, QTextEdit, QLabel, QTableWidget, \
    QTableWidgetItem, QApplication, QColorDialog
from PyQt5.QtCore import QObject, Qt, QPoint
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
        # 连接表头排序函数
        self.tableWidget_main_window.horizontalHeader().sectionClicked.connect(self.HorSectionClicked)
        # 设置表格右键函数
        self.tableWidget_main_window.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键产生子菜单
        self.tableWidget_main_window.customContextMenuRequested.connect(self.generateMenu)  # 右键菜单
        # 设置发报标记的颜色
        self.tableWidget_main_window.itemDoubleClicked.connect(self.SetBackgroundColor)
        # 设置表头日期
        date = self.dateEdit.date().toString(Qt.ISODate)
        dateTomorrow = datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days=1)
        dateToday = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m-%d')
        dateTomorrow = dateTomorrow.strftime('%m-%d')
        self.tableWidget_main_window.setHorizontalHeaderItem(0, QTableWidgetItem(str(dateTomorrow)))
        self.tableWidget_main_window.setHorizontalHeaderItem(1, QTableWidgetItem(str(dateToday)))

    def SetBackgroundColor(self, index):
        row = index.row()
        col = index.column()
        if col == 0 or col == 1:
            color = QColorDialog.getColor()
            if color.isValid():
                self.tableWidget_main_window.item(row, col).setBackground(QColor(color.name()))

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
        date = self.dateEdit.date().toString(Qt.ISODate)


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
                        self.tableWidget_main_window.item(num, 0).setBackground(QColor(dutyinf[0][3]))
                        self.tableWidget_main_window.item(num, 1).setBackground(QColor(dutyinf[0][4]))
                        self.tableWidget_main_window.setItem(num, 5, QTableWidgetItem(str(dutyinf[0][6])))
                        self.tableWidget_main_window.setItem(num, 6, QTableWidgetItem(str(dutyinf[0][7])))
                        self.tableWidget_main_window.item(num, 6).setBackground(QColor(dutyinf[0][5]))

                    Text = QTextEdit()
                    Text.setReadOnly(True)
                    # 获取该航次的需要关注的值班日志
                    sql = f"select * from dutylog where voy = {result[i][4]} and mark = 0"
                    cursor.execute(sql)
                    dutylog = cursor.fetchall()
                    if dutylog:
                        dutylog = list(dutylog)
                        dutylog.reverse()
                        for i in range(len(dutylog)):
                            Text.append(dutylog[i][3].strftime('%Y-%m-%d %H:%M') + ': ' + dutylog[i][4])
                    self.tableWidget_main_window.setCellWidget(num, 7, Text)

    def test(self):
        print('xiugai')
        # print(result[0],result[1])
        #     ViewShipList.append(result)
        # for row in range(len(ViewShipList)):
        #     print(ViewShipList[row])
        # else:
        #     if shiptype ==
        # if ViewShipList:
        #     self.ui_mian.tableWidget_main_window.setRowCount(len(ViewShipList))
        #     for row in range(len(ViewShipList)):
        #         if ViewShipList[row][-1] == 3 or ViewShipList[row][-1] == 4 or ViewShipList[row][-1] == 5:
        #             self.ui_mian.tableWidget_main_window.setItem(row,0,QTableWidgetItem(ViewShipList[row][2]))
        #             print(ViewShipList[row])
        # shiptype =


class LogViewWindow(QtWidgets.QMainWindow, Ui_LogView):
    def __init__(self, shipname, voy):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        # 设置表格右键函数
        self.tableWidget_un.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键产生子菜单
        self.tableWidget_un.customContextMenuRequested.connect(self.generateMenuUn)  # 右键菜单
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
        self.tableWidget_un.setRowCount(len(dutylog))
        if dutylog:
            dutylog = list(dutylog)
            dutylog.reverse()
            for i in range(len(dutylog)):
                self.tableWidget_un.setItem(i, 0, QTableWidgetItem(dutylog[i][3].strftime('%Y-%m-%d %H:%M:%S')))
                self.tableWidget_un.setRowHeight(i, 60)
                Text = QTextEdit()
                Text.setReadOnly(True)
                Text.append(dutylog[i][4])
                self.tableWidget_un.setCellWidget(i, 1, Text)
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
        # 获取该船舶所有航次的值班日志
        sql = f"select voy from dutylog where shipname = '{shipname}' group by voy"
        cursor.execute(sql)
        dutylog = cursor.fetchall()
        for i in range(len(dutylog)):
            self.comboBox.addItem(str(dutylog[i][0]))
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
        db_connect.close()

    def generateMenuUn(self,pos):
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
            self.TextInput = LogInput('添加日志',int(self.comboBox.currentText()))
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
    def __init__(self,title,voy):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(title)
        if self.windowTitle() == '添加日志':
            self.pushButton.setText('确认添加')
        else:
            db_connect = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                         db='cmrcreportsystemdb',
                                         charset='utf8')
            cursor = db_connect.cursor()
            # 查找待解决日志
            sql = f"select * from dutylog where voy = {int(voy)} and date = {self.windowTitle()}"
            cursor.execute(sql)
            dutylog = cursor.fetchall()
            print(dutylog)
            self.pushButton.setText('确认修改')
        self.pushButton.clicked.connect(self.updatelog())
    def updatelog(self):
        log = self.textEdit.toPlainText()
        if self.windowTitle() == '添加日志'

class SendWindow(QtWidgets.QMainWindow, Ui_SendWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.tableWidget_log.setRowCount(100)


#         self.ui_mian.pushButton_update.clicked.connect(self.updatetable)
#         self.ui_mian.pushButton_del.clicked.connect(self.deletetable)
#         # 连接Mysql数据库，读取所有历史值班日期记录
#         db_dutyform = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
#                                             db='dutyform',
#                                             charset='utf8')
#
#         cursor_dutyform = db_dutyform.cursor()
#         sql_dutyform = "SELECT DISTINCT date FROM dutyform"
#         cursor_dutyform.execute(sql_dutyform)
#         result_dutyform = cursor_dutyform.fetchall()
#         duty_list = []
#         for i in range(len(result_dutyform)):
#             duty_list.append(list(result_dutyform[i])[0])
#         self.ui_mian.comboBox.addItems(duty_list)
#         duty_date = self.ui_mian.comboBox.currentText()
#         """
#         1：获取合同库中所有服务中的船舶信息
#         2：更新船舶服务参数数据库
#         """
#         # 连接Mysql合同库s,读取所有服务中船舶信息
#         db_contract = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
#                                             db='contract',
#                                             charset='utf8')
#         cursor_contract = db_contract.cursor()
#         sql_contract = f"select * from contract_list where (service = 0 and running = 0 and inport = 0) " \
#               f"or (service = 0 and running = 1 and inport = 1) or (service = 0 and running = 1 and inport = 0)"
#         cursor_contract.execute(sql_contract)
#         result_contract = cursor_contract.fetchall()
#         self.ui_mian.tableWidget_main_window.setRowCount(len(result_contract))
#         for ship in range(len(result_contract)):
#             sys_voy = result_contract[ship][4]
#             ship_name = result_contract[ship][3]
#             """
#             判断船舶参数表中是否有该航次
#             """
#             sql = "select * from ship_parameter where sys_voy = %s" % sys_voy
#             cursor_contract.execute(sql)
#             result_ship_parameter = cursor_contract.fetchall()
#             if result_ship_parameter:
#                 """
#                 若不存在,则插入新的数据
#                 """
#                 daily_report_interval = 0
#                 five_days_weather_forecast_interval = 999
#                 if result_contract[ship][43] == 0:
#                     three_days_weather_forecast_interval = 999
#                 else:
#                     three_days_weather_forecast_interval = 1
#                 if result_contract[ship][53] == 0 and result_contract[ship][47] == 1 and result_contract[ship][44] == 0:
#                     sys_ship_state = 0
#                 else:
#                     if result_contract[ship][53] == 0 and result_contract[ship][47] == 0 and result_contract[ship][44] == 0:
#                         sys_ship_state = 2
#                     else:
#                         sys_ship_state = 1
#                 manual_ship_state = 999
#                 value = (sys_voy, daily_report_interval, three_days_weather_forecast_interval,
#                          five_days_weather_forecast_interval, sys_ship_state, manual_ship_state)
#                 sql = "INSERT INTO ship_parameter (sys_voy, daily_report_interval," \
#                       " three_days_weather_forecast_interval, five_days_weather_forecast_interval, " \
#                       "sys_ship_state, manual_ship_state) VALUES (%s, %s,%s, %s,%s, %s)"
#                 cursor_contract.execute(sql, value)
#                 db_contract.commit()
#             else:
#                 """
#                      若存在,则更新的数据
#                 """
#                 if result_contract[ship][43] == 0:
#                     three_days_weather_forecast_interval = 999
#                 else:
#                     three_days_weather_forecast_interval = 1
#                 if result_contract[ship][53] == 0 and result_contract[ship][47] == 1 and result_contract[ship][44] == 0:
#                     sys_ship_state = 0
#                 else:
#                     if result_contract[ship][53] == 0 and result_contract[ship][47] == 0 and result_contract[ship][44] == 0:
#                         sys_ship_state = 2
#                     else:
#                         sys_ship_state = 1
#                 if result_ship_parameter[0][5] == sys_ship_state:
#                     manual_ship_state = 999
#                 else:
#                     manual_ship_state = result_ship_parameter[0][5]
#
#                 sql = f"UPDATE ship_parameter set three_days_weather_forecast_interval = " \
#                       f"{three_days_weather_forecast_interval} and sys_ship_state = {sys_ship_state} " \
#                       f"and manual_ship_state = {manual_ship_state} where sys_voy = {sys_voy}"
#                 cursor_contract.execute(sql)
#                 db_contract.commit()
#             """
#             判断该航次是否在值班表中
#             并根据参数表更新值班表
#             """
#             sql = "select * from ship_parameter where sys_voy = %s" % sys_voy
#             cursor_contract.execute(sql)
#             result_ship_parameter = cursor_contract.fetchall()
#             """
#             参数表中该航次数据
#             """
#             daily_report_interval = result_ship_parameter[0][1]
#             three_days_weather_forecast_interval = result_ship_parameter[0][2]
#             five_days_weather_forecast_interval = result_ship_parameter[0][3]
#             sys_ship_state = result_ship_parameter[0][4]
#             manual_ship_state = result_ship_parameter[0][5]
#             """
#             值班表中该航次数据
#             """
#             sql_dutyform_ship = f"select * from dutyform where date = '{duty_date}' and sys_voy = {sys_voy}"
#             cursor_dutyform.execute(sql_dutyform_ship)
#             result_dutyform_ship = cursor_dutyform.fetchall()
#             if result_dutyform_ship:
#                 """
#                 如果在值班表中
#                 更新值班表
#                 """
#                 if three_days_weather_forecast_interval == 999:
#                     sql = f"UPDATE dutyform set three_days_weather_forecast_interval = " \
#                           f"{three_days_weather_forecast_interval} and sys_ship_state = {sys_ship_state} " \
#                           f"and manual_ship_state = {manual_ship_state} where sys_voy = {sys_voy}"
#
#                 sql = f"UPDATE dutyform set three_days_weather_forecast_interval = " \
#                       f"{three_days_weather_forecast_interval} and sys_ship_state = {sys_ship_state} " \
#                       f"and manual_ship_state = {manual_ship_state} where sys_voy = {sys_voy}"
#
#             else:
#                 """
#                 如果不在值班表中
#                 插入值班表
#                 """
#                 date = duty_date
#                 if manual_ship_state == 999:
#                     if sys_ship_state == 1 or sys_ship_state == 2:
#                         three_days_weather_forecast_Date_tomorrow = 0
#                         three_days_weather_forecast_Date_today = 0
#                         five_days_weather_forecast_Date_tomorrow = 0
#                         five_days_weather_forecast_Date_today = 0
#                         ship_state = sys_ship_state
#                         noon_time = None
#                         three_days_weather_forecast = 0
#                         five_days_weather_forecast = 0
#                         daily_report = 0
#                     else:
#                         if daily_report_interval == 999:
#                             daily_report = 0
#                         else:
#                             daily_report = 1
#                 if daily_report_interval == 999:
#                     # 日报不发送
#                     self.ui_mian.tableWidget_main_window.setItem(ship, 10, QTableWidgetItem(''))
#                     self.ui_mian.tableWidget_main_window.item(ship, 10).setTextAlignment(
#                         Qt.AlignHCenter | Qt.AlignVCenter)
#                     self.ui_mian.tableWidget_main_window.item(ship, 10).setBackground(QColor(204, 204, 204))
#                 else:
#                     if daily_report_interval == 0 and result_dutyform_ship[0][12] == 2:
#                         # 日报发送
#                         self.ui_mian.tableWidget_main_window.setItem(ship, 10, QTableWidgetItem('1'))
#                         self.ui_mian.tableWidget_main_window.item(ship, 10).setTextAlignment(
#                             Qt.AlignHCenter | Qt.AlignVCenter)
#                     else:
#                         if daily_report_interval == 0 and result_dutyform_ship[0][12] == 3:
#                             # 日报发送
#                             self.ui_mian.tableWidget_main_window.setItem(ship, 10, QTableWidgetItem('N'))
#                             self.ui_mian.tableWidget_main_window.item(ship, 10).setTextAlignment(
#                                 Qt.AlignHCenter | Qt.AlignVCenter)
#                 if three_days_weather_forecast_interval == 999:
#                     # 三天预报不发送
#
#
#
#
#
#
#
#
#
#
#
#
#             ship_name = result_contract[ship][3]
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#             sql_dutyform_ship = f"select * from dutyform where date = '{duty_date}' and sys_voy = {sys_voy}"
#             cursor_dutyform.execute(sql_dutyform_ship)
#             result_dutyform_ship = cursor_dutyform.fetchall()
#
#             if result_dutyform_ship:
#
#
#
#
#
#
#
#
#
#                 """
#                 先更新值班表中需要更新的字段
#                 若该航次船舶在值班表中，直接填入值班表信息
#                 """
#                 #
#                 three_days_tomorrow_value = result_dutyform_ship[0][2]
#                 three_days_today_value = result_dutyform_ship[0][3]
#                 five_days_tomorrow_value = result_dutyform_ship[0][4]
#                 five_days_today_value = result_dutyform_ship[0][5]
#                 ship_state_value = result_dutyform_ship[0][8]
#                 # 明天
#                 self.ui_mian.tableWidget_main_window.horizontalHeaderItem(0).setText(
#                     (datetime.datetime.strptime(duty_date,'%Y-%m-%d')+datetime.timedelta(days=1)).strftime('%d')+'(三天)')
#                 self.ui_mian.tableWidget_main_window.setItem(ship,0,QTableWidgetItem(three_days_tomorrow_dict[three_days_tomorrow_value][0]))
#                 self.ui_mian.tableWidget_main_window.item(ship, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#                 self.ui_mian.tableWidget_main_window.item(ship, 0).setBackground(QBrush(three_days_tomorrow_dict[three_days_tomorrow_value][1]))
#                 #今天
#                 self.ui_mian.tableWidget_main_window.horizontalHeaderItem(1).setText(
#                     (datetime.datetime.strptime(duty_date, '%Y-%m-%d')).strftime('%d')+'(三天)')
#                 self.ui_mian.tableWidget_main_window.setItem(ship,1,QTableWidgetItem(three_days_tomorrow_dict[three_days_today_value][0]))
#                 self.ui_mian.tableWidget_main_window.item(ship, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#                 self.ui_mian.tableWidget_main_window.item(ship, 1).setBackground(QBrush(three_days_today_dict[three_days_today_value][1]))
#                 # 明天
#                 self.ui_mian.tableWidget_main_window.horizontalHeaderItem(2).setText(
#                     (datetime.datetime.strptime(duty_date,'%Y-%m-%d')+datetime.timedelta(days=1)).strftime('%d')+'(五天)')
#                 self.ui_mian.tableWidget_main_window.setItem(ship,2,QTableWidgetItem(five_days_tomorrow_dict[five_days_tomorrow_value][0]))
#                 self.ui_mian.tableWidget_main_window.item(ship, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#                 self.ui_mian.tableWidget_main_window.item(ship, 2).setBackground(QBrush(five_days_tomorrow_dict[five_days_tomorrow_value][1]))
#                 #今天
#                 self.ui_mian.tableWidget_main_window.horizontalHeaderItem(3).setText(
#                     (datetime.datetime.strptime(duty_date, '%Y-%m-%d')).strftime('%d')+'(五天)')
#                 self.ui_mian.tableWidget_main_window.setItem(ship,3,QTableWidgetItem(five_days_today_dict[five_days_today_value][0]))
#                 self.ui_mian.tableWidget_main_window.item(ship, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#                 self.ui_mian.tableWidget_main_window.item(ship, 3).setBackground(QBrush(five_days_today_dict[five_days_today_value][1]))
#                 #船名
#                 self.ui_mian.tableWidget_main_window.setItem(ship,4,QTableWidgetItem(ship_name))
#                 self.ui_mian.tableWidget_main_window.item(ship, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#                 self.ui_mian.tableWidget_main_window.item(ship, 4).setBackground(QBrush(ship_state_dict[ship_state_value]))
#                 #航次号
#                 self.ui_mian.tableWidget_main_window.setItem(ship,5,QTableWidgetItem(str(sys_voy)))
#                 self.ui_mian.tableWidget_main_window.item(ship, 5).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#         print(result_contract)
#         print(len(result_contract))
#
#         """
#             默认选中的是服务中船舶
#             读取最新的Mysql里的合同库获取所有服务中船舶
#         """
#         service_ship_list = [1, 2]
#         for ship in range(len(service_ship_list)):
#             ship_line = service_ship_list[ship]
#             # 根据航次号,读取值班表里的信息
#             ship_inf = []
#             if ship_inf:
#                 # 读取最新的Mysql里的值班表并写入tableWidget_main_window
#                 print('xieru')
#             else:
#                 # 不在值班表里的船舶，新服务的航次，整行显示红色，人工设置船舶发报参数，默认第一次发预报，发日报
#                 print('new')
#
#         # 右键菜单
#         self.ui_mian.tableWidget_main_window.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
#         self.ui_mian.tableWidget_main_window.customContextMenuRequested.connect(self.generateMenu)  ####右键菜单
#
#     def open_ship_parameter(self, index):
#         sys_voy = self.ui_mian.tableWidget_main_window.item(index.row(), 5).text()
#         self.set_ship_parameter_window = set_ship_parameter(sys_voy)
#         self.set_ship_parameter_window.show()
#
#     def generateMenu(self, pos):
#         row_num = -1
#         for i in self.ui_mian.tableWidget_main_window.selectionModel().selection().indexes():
#             row_num = i.row()
#         menu = QMenu()
#         item1 = menu.addAction(u"日报")
#         item2 = menu.addAction(u"三天预报")
#         item3 = menu.addAction(u"五天预报")
#         item3 = menu.addAction(u"台风报")
#         item3 = menu.addAction(u"其他报文")
#         item4 = menu.addAction(u"船舶参数设置")
#         action = menu.exec_(self.ui_mian.tableWidget_main_window.mapToGlobal(pos))
#         if action == item4:
#             sys_voy = self.ui_mian.tableWidget_main_window.item(row_num, 5).text()
#             ship_name = self.ui_mian.tableWidget_main_window.item(row_num, 4).text()
#             self.set_ship_parameter_window = set_ship_parameter(sys_voy, ship_name)
#             self.set_ship_parameter_window.show()
#
#     """
#     根据当前日期，更新值班表格
#     """
#
#     def updatetable(self):
#         print('1')
#
#     """
#     删除当前日期的值班表格
#     """
#
#     def deletetable(self):
#         print('1')
#
# # 船舶参数界面
# class set_ship_parameter(QtWidgets.QWidget, Ui_SetShipParameter):
#     def __init__(self, sys_voy, ship_name):
#         super(set_ship_parameter, self).__init__()
#         self.setupUi(self)
#         self.setWindowTitle(ship_name + '：参数设置')
#         self.label.setText(sys_voy)
#         # 读取MySQL数据库中船舶参数
#         db_ship_parameter = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
#                                             db='contract',
#                                             charset='utf8')
#         cursor = db_ship_parameter.cursor()
#         sql = "select * from ship_parameter where sys_voy = %s" % sys_voy
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         if not result:
#             sql = f"select * from contract_list where voyage_no = {sys_voy}"
#             cursor.execute(sql)
#             ship_inf = cursor.fetchall()
#             daily_report_interval = 0
#             five_days_weather_forecast_interval = 999
#             if ship_inf[0][43] == 0:
#                 three_days_weather_forecast_interval = 999
#             else:
#                 three_days_weather_forecast_interval = 1
#             if ship_inf[0][53] == 0 and ship_inf[0][47] == 1 and ship_inf[0][44] == 0:
#                 sys_ship_state = 0
#             else:
#                 if ship_inf[0][53] == 0 and ship_inf[0][47] == 0 and ship_inf[0][44] == 0:
#                     sys_ship_state = 2
#                 else:
#                     sys_ship_state = 1
#             manual_ship_state = 999
#             value = (sys_voy, daily_report_interval, three_days_weather_forecast_interval,
#                      five_days_weather_forecast_interval, sys_ship_state, manual_ship_state)
#             sql = "INSERT INTO ship_parameter (sys_voy, daily_report_interval," \
#                   " three_days_weather_forecast_interval, five_days_weather_forecast_interval, " \
#                   "sys_ship_state, manual_ship_state) VALUES (%s, %s,%s, %s,%s, %s)"
#             cursor.execute(sql, value)
#             db_ship_parameter.commit()
#         else:
#             daily_report_interval = result[0][1]
#             three_days_weather_forecast_interval = result[0][2]
#             five_days_weather_forecast_interval = result[0][3]
#             sys_ship_state = result[0][4]
#             manual_ship_state = result[0][5]
#         # 显示当前参数
#         self.comboBox_daily_report.setCurrentIndex(self.comboBox_daily_report.findText(str(daily_report_interval)))
#         self.comboBox_three_days.setCurrentIndex(
#             self.comboBox_three_days.findText(str(three_days_weather_forecast_interval)))
#         self.comboBox_five_days.setCurrentIndex(
#             self.comboBox_five_days.findText(str(five_days_weather_forecast_interval)))
#         self.comboBox_4.setCurrentIndex(
#             self.comboBox_4.findText(str(sys_ship_state)))
#         self.comboBox_manual.setCurrentIndex(
#             self.comboBox_manual.findText(str(manual_ship_state)))
#         db_ship_parameter.close()
#         # 船舶参数设置界面连接的函数
#         self.comboBox_daily_report.currentIndexChanged.connect(lambda: self.daily_report_update(sys_voy))
#         self.comboBox_three_days.currentIndexChanged.connect(lambda: self.three_days_update(sys_voy))
#         self.comboBox_five_days.currentIndexChanged.connect(lambda: self.five_days_update(sys_voy))
#         self.comboBox_manual.currentIndexChanged.connect(lambda: self.manual_update(sys_voy))
#
#     def daily_report_update(self, sys_voy):
#         db_ship_parameter = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
#                                             db='contract',
#                                             charset='utf8')
#         cursor = db_ship_parameter.cursor()
#         daily_report_interval = self.comboBox_daily_report.currentText()
#         sql = f"UPDATE ship_parameter set daily_report_interval = {int(daily_report_interval)} where sys_voy = {sys_voy}"
#         cursor.execute(sql)
#         db_ship_parameter.commit()
#         db_ship_parameter.close()
#
#     def three_days_update(self, sys_voy):
#         db_ship_parameter = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
#                                             db='contract',
#                                             charset='utf8')
#         cursor = db_ship_parameter.cursor()
#         three_days_weather_forecast_interval = self.comboBox_three_days.currentText()
#         sql = f"UPDATE ship_parameter set three_days_weather_forecast_interval = {int(three_days_weather_forecast_interval)} where sys_voy = {sys_voy}"
#         cursor.execute(sql)
#         db_ship_parameter.commit()
#         db_ship_parameter.close()
#
#     def five_days_update(self, sys_voy):
#         db_ship_parameter = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
#                                             db='contract',
#                                             charset='utf8')
#         cursor = db_ship_parameter.cursor()
#         five_days_weather_forecast_interval = self.comboBox_five_days.currentText()
#         sql = f"UPDATE ship_parameter set five_days_weather_forecast_interval = {int(five_days_weather_forecast_interval)} where sys_voy = {sys_voy}"
#         cursor.execute(sql)
#         db_ship_parameter.commit()
#         db_ship_parameter.close()
#
#     def manual_update(self, sys_voy):
#         db_ship_parameter = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
#                                             db='contract',
#                                             charset='utf8')
#         cursor = db_ship_parameter.cursor()
#         manual_ship_state = self.comboBox_manual.currentText()
#         sql = f"UPDATE ship_parameter set manual_ship_state = {int(manual_ship_state)} where sys_voy = {sys_voy}"
#         cursor.execute(sql)
#         db_ship_parameter.commit()
#         db_ship_parameter.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(SortUporDown)
    window.show()
    sys.exit(app.exec_())
