import datetime

import pymysql
from PyQt5.QtGui import QBrush, QColor

from ReportSystem.UiCode.Ui_ShipParameter import Ui_SetShipParameter
from UiCode.Ui_MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMessageBox, QInputDialog, QLineEdit, QMenu, QTextEdit, QLabel, QTableWidget, \
    QTableWidgetItem
from PyQt5.QtCore import QObject, Qt
import sys


three_days_tomorrow_dict = {
    0:['',QColor(204, 204, 204)],
    1:['√',QColor(255, 255, 0)]
}

three_days_today_dict = {
    0: ['', QColor(204, 204, 204)],
    1: ['√', QColor(106, 168, 79)]
}
five_days_tomorrow_dict = {
    0: ['', QColor(204, 204, 204)],
    1: ['√', QColor(0, 255, 255)]
}

five_days_today_dict = {
    0: ['', QColor(204, 204, 204)],
    1: ['√', QColor(255, 153, 0)]
}

ship_state_dict = {
    0: QColor(255, 255, 255),
    1: QColor(153, 0, 255),
    2: QColor(153, 0, 255)
}

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui_mian = Ui_MainWindow()
        self.ui_mian.setupUi(self)
        self.ui_mian.pushButton_update.clicked.connect(self.updatetable)
        self.ui_mian.pushButton_del.clicked.connect(self.deletetable)
        # 连接Mysql数据库，读取所有历史值班日期记录
        db_dutyform = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                            db='dutyform',
                                            charset='utf8')

        cursor_dutyform = db_dutyform.cursor()
        sql_dutyform = "SELECT DISTINCT date FROM dutyform"
        cursor_dutyform.execute(sql_dutyform)
        result_dutyform = cursor_dutyform.fetchall()
        duty_list = []
        for i in range(len(result_dutyform)):
            duty_list.append(list(result_dutyform[i])[0])
        self.ui_mian.comboBox.addItems(duty_list)
        duty_date = self.ui_mian.comboBox.currentText()
        """
        1：获取合同库中所有服务中的船舶信息
        2：更新船舶服务参数数据库
        """
        # 连接Mysql合同库s,读取所有服务中船舶信息
        db_contract = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                            db='contract',
                                            charset='utf8')
        cursor_contract = db_contract.cursor()
        sql_contract = f"select * from contract_list where (service = 0 and running = 0 and inport = 0) " \
              f"or (service = 0 and running = 1 and inport = 1) or (service = 0 and running = 1 and inport = 0)"
        cursor_contract.execute(sql_contract)
        result_contract = cursor_contract.fetchall()
        self.ui_mian.tableWidget_main_window.setRowCount(len(result_contract))
        for ship in range(len(result_contract)):
            sys_voy = result_contract[ship][4]
            ship_name = result_contract[ship][3]
            """
            判断船舶参数表中是否有该航次
            """
            sql = "select * from ship_parameter where sys_voy = %s" % sys_voy
            cursor_contract.execute(sql)
            result_ship_parameter = cursor_contract.fetchall()
            if result_ship_parameter:
                """
                若不存在,则插入新的数据
                """
                daily_report_interval = 0
                five_days_weather_forecast_interval = 999
                if result_contract[ship][43] == 0:
                    three_days_weather_forecast_interval = 999
                else:
                    three_days_weather_forecast_interval = 1
                if result_contract[ship][53] == 0 and result_contract[ship][47] == 1 and result_contract[ship][44] == 0:
                    sys_ship_state = 0
                else:
                    if result_contract[ship][53] == 0 and result_contract[ship][47] == 0 and result_contract[ship][44] == 0:
                        sys_ship_state = 2
                    else:
                        sys_ship_state = 1
                manual_ship_state = 999
                value = (sys_voy, daily_report_interval, three_days_weather_forecast_interval,
                         five_days_weather_forecast_interval, sys_ship_state, manual_ship_state)
                sql = "INSERT INTO ship_parameter (sys_voy, daily_report_interval," \
                      " three_days_weather_forecast_interval, five_days_weather_forecast_interval, " \
                      "sys_ship_state, manual_ship_state) VALUES (%s, %s,%s, %s,%s, %s)"
                cursor_contract.execute(sql, value)
                db_contract.commit()
            else:
                """
                     若存在,则更新的数据
                """
                if result_contract[ship][43] == 0:
                    three_days_weather_forecast_interval = 999
                else:
                    three_days_weather_forecast_interval = 1
                if result_contract[ship][53] == 0 and result_contract[ship][47] == 1 and result_contract[ship][44] == 0:
                    sys_ship_state = 0
                else:
                    if result_contract[ship][53] == 0 and result_contract[ship][47] == 0 and result_contract[ship][44] == 0:
                        sys_ship_state = 2
                    else:
                        sys_ship_state = 1
                if result_ship_parameter[0][5] == sys_ship_state:
                    manual_ship_state = 999
                else:
                    manual_ship_state = result_ship_parameter[0][5]

                sql = f"UPDATE ship_parameter set three_days_weather_forecast_interval = " \
                      f"{three_days_weather_forecast_interval} and sys_ship_state = {sys_ship_state} " \
                      f"and manual_ship_state = {manual_ship_state} where sys_voy = {sys_voy}"
                cursor_contract.execute(sql)
                db_contract.commit()
            """
            判断该航次是否在值班表中
            并根据参数表更新值班表
            """
            sql = "select * from ship_parameter where sys_voy = %s" % sys_voy
            cursor_contract.execute(sql)
            result_ship_parameter = cursor_contract.fetchall()
            """
            参数表中该航次数据
            """
            daily_report_interval = result_ship_parameter[0][1]
            three_days_weather_forecast_interval = result_ship_parameter[0][2]
            five_days_weather_forecast_interval = result_ship_parameter[0][3]
            sys_ship_state = result_ship_parameter[0][4]
            manual_ship_state = result_ship_parameter[0][5]
            """
            值班表中该航次数据
            """
            sql_dutyform_ship = f"select * from dutyform where date = '{duty_date}' and sys_voy = {sys_voy}"
            cursor_dutyform.execute(sql_dutyform_ship)
            result_dutyform_ship = cursor_dutyform.fetchall()
            if result_dutyform_ship:
                """
                如果在值班表中
                更新值班表
                """
                if three_days_weather_forecast_interval == 999:
                    sql = f"UPDATE dutyform set three_days_weather_forecast_interval = " \
                          f"{three_days_weather_forecast_interval} and sys_ship_state = {sys_ship_state} " \
                          f"and manual_ship_state = {manual_ship_state} where sys_voy = {sys_voy}"

                sql = f"UPDATE dutyform set three_days_weather_forecast_interval = " \
                      f"{three_days_weather_forecast_interval} and sys_ship_state = {sys_ship_state} " \
                      f"and manual_ship_state = {manual_ship_state} where sys_voy = {sys_voy}"

            else:
                """
                如果不在值班表中
                插入值班表
                """
                date = duty_date
                if manual_ship_state == 999:
                    if sys_ship_state == 1 or sys_ship_state == 2:
                        three_days_weather_forecast_Date_tomorrow = 0
                        three_days_weather_forecast_Date_today = 0
                        five_days_weather_forecast_Date_tomorrow = 0
                        five_days_weather_forecast_Date_today = 0
                        ship_state = sys_ship_state
                        noon_time = None
                        three_days_weather_forecast = 0
                        five_days_weather_forecast = 0
                        daily_report = 0
                    else:
                        if daily_report_interval == 999:
                            daily_report = 0
                        else:
                            daily_report = 1
                        if three_days_weather_ forecast_interval
                # if daily_report_interval == 999:
                #     # 日报不发送
                #     self.ui_mian.tableWidget_main_window.setItem(ship, 10, QTableWidgetItem(''))
                #     self.ui_mian.tableWidget_main_window.item(ship, 10).setTextAlignment(
                #         Qt.AlignHCenter | Qt.AlignVCenter)
                #     self.ui_mian.tableWidget_main_window.item(ship, 10).setBackground(QColor(204, 204, 204))
                # else:
                #     if daily_report_interval == 0 and result_dutyform_ship[0][12] == 2:
                #         # 日报发送
                #         self.ui_mian.tableWidget_main_window.setItem(ship, 10, QTableWidgetItem('1'))
                #         self.ui_mian.tableWidget_main_window.item(ship, 10).setTextAlignment(
                #             Qt.AlignHCenter | Qt.AlignVCenter)
                #     else:
                #         if daily_report_interval == 0 and result_dutyform_ship[0][12] == 3:
                #             # 日报发送
                #             self.ui_mian.tableWidget_main_window.setItem(ship, 10, QTableWidgetItem('N'))
                #             self.ui_mian.tableWidget_main_window.item(ship, 10).setTextAlignment(
                #                 Qt.AlignHCenter | Qt.AlignVCenter)
                # if three_days_weather_forecast_interval == 999:
                #     # 三天预报不发送











        #
        #     ship_name = result_contract[ship][3]
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
        #     sql_dutyform_ship = f"select * from dutyform where date = '{duty_date}' and sys_voy = {sys_voy}"
        #     cursor_dutyform.execute(sql_dutyform_ship)
        #     result_dutyform_ship = cursor_dutyform.fetchall()
        #
        #     if result_dutyform_ship:
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #         """
        #         先更新值班表中需要更新的字段
        #         若该航次船舶在值班表中，直接填入值班表信息
        #         """
        #         #
        #         three_days_tomorrow_value = result_dutyform_ship[0][2]
        #         three_days_today_value = result_dutyform_ship[0][3]
        #         five_days_tomorrow_value = result_dutyform_ship[0][4]
        #         five_days_today_value = result_dutyform_ship[0][5]
        #         ship_state_value = result_dutyform_ship[0][8]
        #         # 明天
        #         self.ui_mian.tableWidget_main_window.horizontalHeaderItem(0).setText(
        #             (datetime.datetime.strptime(duty_date,'%Y-%m-%d')+datetime.timedelta(days=1)).strftime('%d')+'(三天)')
        #         self.ui_mian.tableWidget_main_window.setItem(ship,0,QTableWidgetItem(three_days_tomorrow_dict[three_days_tomorrow_value][0]))
        #         self.ui_mian.tableWidget_main_window.item(ship, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #         self.ui_mian.tableWidget_main_window.item(ship, 0).setBackground(QBrush(three_days_tomorrow_dict[three_days_tomorrow_value][1]))
        #         #今天
        #         self.ui_mian.tableWidget_main_window.horizontalHeaderItem(1).setText(
        #             (datetime.datetime.strptime(duty_date, '%Y-%m-%d')).strftime('%d')+'(三天)')
        #         self.ui_mian.tableWidget_main_window.setItem(ship,1,QTableWidgetItem(three_days_tomorrow_dict[three_days_today_value][0]))
        #         self.ui_mian.tableWidget_main_window.item(ship, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #         self.ui_mian.tableWidget_main_window.item(ship, 1).setBackground(QBrush(three_days_today_dict[three_days_today_value][1]))
        #         # 明天
        #         self.ui_mian.tableWidget_main_window.horizontalHeaderItem(2).setText(
        #             (datetime.datetime.strptime(duty_date,'%Y-%m-%d')+datetime.timedelta(days=1)).strftime('%d')+'(五天)')
        #         self.ui_mian.tableWidget_main_window.setItem(ship,2,QTableWidgetItem(five_days_tomorrow_dict[five_days_tomorrow_value][0]))
        #         self.ui_mian.tableWidget_main_window.item(ship, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #         self.ui_mian.tableWidget_main_window.item(ship, 2).setBackground(QBrush(five_days_tomorrow_dict[five_days_tomorrow_value][1]))
        #         #今天
        #         self.ui_mian.tableWidget_main_window.horizontalHeaderItem(3).setText(
        #             (datetime.datetime.strptime(duty_date, '%Y-%m-%d')).strftime('%d')+'(五天)')
        #         self.ui_mian.tableWidget_main_window.setItem(ship,3,QTableWidgetItem(five_days_today_dict[five_days_today_value][0]))
        #         self.ui_mian.tableWidget_main_window.item(ship, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #         self.ui_mian.tableWidget_main_window.item(ship, 3).setBackground(QBrush(five_days_today_dict[five_days_today_value][1]))
        #         #船名
        #         self.ui_mian.tableWidget_main_window.setItem(ship,4,QTableWidgetItem(ship_name))
        #         self.ui_mian.tableWidget_main_window.item(ship, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #         self.ui_mian.tableWidget_main_window.item(ship, 4).setBackground(QBrush(ship_state_dict[ship_state_value]))
        #         #航次号
        #         self.ui_mian.tableWidget_main_window.setItem(ship,5,QTableWidgetItem(str(sys_voy)))
        #         self.ui_mian.tableWidget_main_window.item(ship, 5).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # print(result_contract)
        # print(len(result_contract))

        """
            默认选中的是服务中船舶
            读取最新的Mysql里的合同库获取所有服务中船舶
        """
        service_ship_list = [1, 2]
        for ship in range(len(service_ship_list)):
            ship_line = service_ship_list[ship]
            # 根据航次号,读取值班表里的信息
            ship_inf = []
            if ship_inf:
                # 读取最新的Mysql里的值班表并写入tableWidget_main_window
                print('xieru')
            else:
                # 不在值班表里的船舶，新服务的航次，整行显示红色，人工设置船舶发报参数，默认第一次发预报，发日报
                print('new')

        # 右键菜单
        self.ui_mian.tableWidget_main_window.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.ui_mian.tableWidget_main_window.customContextMenuRequested.connect(self.generateMenu)  ####右键菜单

    def open_ship_parameter(self, index):
        sys_voy = self.ui_mian.tableWidget_main_window.item(index.row(), 5).text()
        self.set_ship_parameter_window = set_ship_parameter(sys_voy)
        self.set_ship_parameter_window.show()

    def generateMenu(self, pos):
        row_num = -1
        for i in self.ui_mian.tableWidget_main_window.selectionModel().selection().indexes():
            row_num = i.row()
        menu = QMenu()
        item1 = menu.addAction(u"日报")
        item2 = menu.addAction(u"三天预报")
        item3 = menu.addAction(u"五天预报")
        item3 = menu.addAction(u"台风报")
        item3 = menu.addAction(u"其他报文")
        item4 = menu.addAction(u"船舶参数设置")
        action = menu.exec_(self.ui_mian.tableWidget_main_window.mapToGlobal(pos))
        if action == item4:
            sys_voy = self.ui_mian.tableWidget_main_window.item(row_num, 5).text()
            ship_name = self.ui_mian.tableWidget_main_window.item(row_num, 4).text()
            self.set_ship_parameter_window = set_ship_parameter(sys_voy, ship_name)
            self.set_ship_parameter_window.show()

    """
    根据当前日期，更新值班表格
    """

    def updatetable(self):
        print('1')

    """
    删除当前日期的值班表格
    """

    def deletetable(self):
        print('1')

# 船舶参数界面
class set_ship_parameter(QtWidgets.QWidget, Ui_SetShipParameter):
    def __init__(self, sys_voy, ship_name):
        super(set_ship_parameter, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(ship_name + '：参数设置')
        self.label.setText(sys_voy)
        # 读取MySQL数据库中船舶参数
        db_ship_parameter = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                            db='contract',
                                            charset='utf8')
        cursor = db_ship_parameter.cursor()
        sql = "select * from ship_parameter where sys_voy = %s" % sys_voy
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            sql = f"select * from contract_list where voyage_no = {sys_voy}"
            cursor.execute(sql)
            ship_inf = cursor.fetchall()
            daily_report_interval = 0
            five_days_weather_forecast_interval = 999
            if ship_inf[0][43] == 0:
                three_days_weather_forecast_interval = 999
            else:
                three_days_weather_forecast_interval = 1
            if ship_inf[0][53] == 0 and ship_inf[0][47] == 1 and ship_inf[0][44] == 0:
                sys_ship_state = 0
            else:
                if ship_inf[0][53] == 0 and ship_inf[0][47] == 0 and ship_inf[0][44] == 0:
                    sys_ship_state = 2
                else:
                    sys_ship_state = 1
            manual_ship_state = 999
            value = (sys_voy, daily_report_interval, three_days_weather_forecast_interval,
                     five_days_weather_forecast_interval, sys_ship_state, manual_ship_state)
            sql = "INSERT INTO ship_parameter (sys_voy, daily_report_interval," \
                  " three_days_weather_forecast_interval, five_days_weather_forecast_interval, " \
                  "sys_ship_state, manual_ship_state) VALUES (%s, %s,%s, %s,%s, %s)"
            cursor.execute(sql, value)
            db_ship_parameter.commit()
        else:
            daily_report_interval = result[0][1]
            three_days_weather_forecast_interval = result[0][2]
            five_days_weather_forecast_interval = result[0][3]
            sys_ship_state = result[0][4]
            manual_ship_state = result[0][5]
        # 显示当前参数
        self.comboBox_daily_report.setCurrentIndex(self.comboBox_daily_report.findText(str(daily_report_interval)))
        self.comboBox_three_days.setCurrentIndex(
            self.comboBox_three_days.findText(str(three_days_weather_forecast_interval)))
        self.comboBox_five_days.setCurrentIndex(
            self.comboBox_five_days.findText(str(five_days_weather_forecast_interval)))
        self.comboBox_4.setCurrentIndex(
            self.comboBox_4.findText(str(sys_ship_state)))
        self.comboBox_manual.setCurrentIndex(
            self.comboBox_manual.findText(str(manual_ship_state)))
        db_ship_parameter.close()
        # 船舶参数设置界面连接的函数
        self.comboBox_daily_report.currentIndexChanged.connect(lambda: self.daily_report_update(sys_voy))
        self.comboBox_three_days.currentIndexChanged.connect(lambda: self.three_days_update(sys_voy))
        self.comboBox_five_days.currentIndexChanged.connect(lambda: self.five_days_update(sys_voy))
        self.comboBox_manual.currentIndexChanged.connect(lambda: self.manual_update(sys_voy))

    def daily_report_update(self, sys_voy):
        db_ship_parameter = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                            db='contract',
                                            charset='utf8')
        cursor = db_ship_parameter.cursor()
        daily_report_interval = self.comboBox_daily_report.currentText()
        sql = f"UPDATE ship_parameter set daily_report_interval = {int(daily_report_interval)} where sys_voy = {sys_voy}"
        cursor.execute(sql)
        db_ship_parameter.commit()
        db_ship_parameter.close()

    def three_days_update(self, sys_voy):
        db_ship_parameter = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                            db='contract',
                                            charset='utf8')
        cursor = db_ship_parameter.cursor()
        three_days_weather_forecast_interval = self.comboBox_three_days.currentText()
        sql = f"UPDATE ship_parameter set three_days_weather_forecast_interval = {int(three_days_weather_forecast_interval)} where sys_voy = {sys_voy}"
        cursor.execute(sql)
        db_ship_parameter.commit()
        db_ship_parameter.close()

    def five_days_update(self, sys_voy):
        db_ship_parameter = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                            db='contract',
                                            charset='utf8')
        cursor = db_ship_parameter.cursor()
        five_days_weather_forecast_interval = self.comboBox_five_days.currentText()
        sql = f"UPDATE ship_parameter set five_days_weather_forecast_interval = {int(five_days_weather_forecast_interval)} where sys_voy = {sys_voy}"
        cursor.execute(sql)
        db_ship_parameter.commit()
        db_ship_parameter.close()

    def manual_update(self, sys_voy):
        db_ship_parameter = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507',
                                            db='contract',
                                            charset='utf8')
        cursor = db_ship_parameter.cursor()
        manual_ship_state = self.comboBox_manual.currentText()
        sql = f"UPDATE ship_parameter set manual_ship_state = {int(manual_ship_state)} where sys_voy = {sys_voy}"
        cursor.execute(sql)
        db_ship_parameter.commit()
        db_ship_parameter.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
