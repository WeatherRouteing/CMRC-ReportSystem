from UiCode.Ui_MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QMessageBox,QInputDialog,QLineEdit,QMenu,QTextEdit,QLabel
from PyQt5.QtCore import QObject, Qt
import sys
# dict_list {
#     'dailyreport_no_send':'灰色',
#     'ship_in_port':'紫色',
#     'tree_days_weather_forcast':'绿色',
#     'five_days_weather_forcast': '淡蓝色',
#     'three_and_five_days_weather_forcast':'黄色'
#     }

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui_mian = Ui_MainWindow()
        self.ui_mian.setupUi(self)
        self.ui_mian.pushButton_update.clicked.connect(self.updatetable)
        self.ui_mian.pushButton_del.clicked.connect(self.deletetable)
        # 连接Mysql数据库，读取所有历史值班日期记录
        result = ['2021-07-10','2021-07-9','2021-07-08','2021-07-07','2021-07-06','2021-07-05']
        self.ui_mian.comboBox.addItems(result)
        self.ui_mian.tableWidget_main_window.setRowCount(10)


        """
        添加文本编辑，选中文本，右键菜单功能
        """
        textEdit=QTextEdit()
        
        textEdit.setMinimumHeight(200)
        tc = textEdit.textCursor()
        text = tc.selectedText()
        textEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        print(text)
        if text != '':
            
            textEdit.customContextMenuRequested[QtCore.QPoint].connect(self.texthighlit)


        self.ui_mian.tableWidget_main_window.setCellWidget(1, 7, textEdit)
        """
            默认选中的是服务中船舶
            读取最新的Mysql里的合同库获取所有服务中船舶
        """
        service_ship_list = [1,2]
        for ship in range(len(service_ship_list)):
            ship_line = service_ship_list[ship]
            # 根据航次号,读取值班表里的信息
            ship_inf = []
            if ship_inf:
                #读取最新的Mysql里的值班表并写入tableWidget_main_window
                print('xieru')
            else:
                #不在值班表里的船舶，新服务的航次，整行显示红色，人工设置船舶发报参数，默认第一次发预报，发日报
                print('new')
        
        # 右键菜单
        self.ui_mian.tableWidget_main_window.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.ui_mian.tableWidget_main_window.customContextMenuRequested.connect(self.generateMenu)  ####右键菜单

    def generateMenu(self, pos):
        print( pos)
        row_num = -1
        for i in self.ui_mian.tableWidget_main_window.selectionModel().selection().indexes():
            row_num = i.row()
        print(row_num)
        menu = QMenu()
        item1 = menu.addAction(u"日报")
        item2 = menu.addAction(u"三天预报")
        item3 = menu.addAction(u"五天预报")
        item3 = menu.addAction(u"台风报")
        item3 = menu.addAction(u"其他报文")
        action = menu.exec_(self.ui_mian.tableWidget_main_window.mapToGlobal(pos))
        #if row_num < 2:
    def texthighlit(self, pos):
        # tc = textEdit.textCursor()
        # print(tc.selectedText())#打印出所选择的文本
        # tc.removeSelectedText()
        # textEdit.setFocus()

        print( pos)
        row_num = -1
        for i in self.ui_mian.tableWidget_main_window.selectionModel().selection().indexes():
            row_num = i.row()
        print(row_num)
        menu = QMenu()
        item1 = menu.addAction(u"添加标记")
        item2 = menu.addAction(u"取消标记")


        action = menu.exec_(self.ui_mian.tableWidget_main_window.mapToGlobal(pos))
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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())