from PyQt5.Qt import *
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QTextEdit_文本光标')
        self.resize(500, 500)
        self.iniUI()

    def iniUI(self):
        te = QTextEdit(self)
        self.te = te
        te.resize(self.width() * 7 / 8, self.height() * 7 / 8)
        te.move((self.width() - te.width()) / 2, 2)
        te.setStyleSheet('background-color:cyan;font-size:20px')
        te.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        btn = QPushButton(self)
        self.btn = btn
        self.btn_w = self.width() / 3
        self.btn_h = self.height() * 3 / 32
        self.btn.resize(self.btn_w, self.btn_h)
        self.btn_x = (self.width() - self.btn_w) / 2
        self.btn_y = self.height() * 7 / 8 + (self.height() / 8 - self.btn_h) / 2
        self.btn.setText('测试按钮')
        self.btn.setStyleSheet('font-size:30px')
        self.btn.move(self.btn_x, self.btn_y)


    def textGet_choosen(self):
        tc = self.te.textCursor()
        print(tc.selectedText())#打印出所选择的文本
        print(tc.selection().toPlainText()) # QDocumentFragment
        # 返回选中的表格的区域位置及大小，由四个元素组成的元组，
        # ( 左上元素行号， 选中的行数，左上元素列号，选中的列数 )
        print(tc.selectedTableCells())

        print(tc.selectionStart())#所选中内容 的位置
        print(tc.selectionEnd())

        #############################################取消选中
        # tc.clearSeletion()
        # self.te.setCursor(tc)#需要反向设置，因为光标取消了选中，所以需要重新设置光标


        ##################移除所选中的文本
        tc.removeSelectedText()
        self.te.setFocus()
    ##########################################################删除 特定文本（纯代码操作删除）




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MyWindow()

    win.btn.clicked.connect(win.textGet_choosen)
    win.show()
    sys.exit(app.exec_())
