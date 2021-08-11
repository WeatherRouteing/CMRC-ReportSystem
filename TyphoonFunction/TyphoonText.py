# -*- coding: utf8 -*-
# @Project     : viewTyphoonText
# @FileName    : TyphoonText.py
# @Time        : 2021/3/24 10:11
# @Author      : Gore
import pymysql

class TyphoonText():
    def __init__(self,initialTime,forecastType):
        self.initialTime = initialTime  #2021-01-01 00:00:00
        self.forecastType = forecastType
        self.TyphoonText = ()
        self.FCT_cnToenDict = \
        {"中央气象台":"BABJWTPQ","日本主观":"RJTDSUBJ","美国主观":"PGTWSUBJ","韩国主观":"RKSLWTKO","印度主观":"DEMSSUBJ","美国大西洋":"KNHCSUBJ",
         "南印度洋":"FMEEWTIO","美国中太":"PHNCSUBJ","澳大利亚":"APRFWTAU","斐济主观":"NFFNWTPS","GRAPESTYM":"GRAPES_T","EC确定":"ECMFJSXX",
         "NCEP确定":"NCEPAVNO","日本全模":"RJTDGLML","日本集合":"RJTDTYES","英国全模":"EGRR","北京模式":"BABJOBJE","集合订正": "BABJEEMD",
         "上海集合":"BCSHWOCI","香港":"BEHKWOCI","广东综合":"BCGZWOCI","广西":"BENNWOCI","福建":"BEFZWOCI","江苏":"BENJWOCI"}

    def SelectDB(self):
        sql = self.FilmSql()
        conn = pymysql.connect(host="10.20.65.62", user="tfk", password="GlobalTyphoon62!", database="micapsdataserver")
        cursor = conn.cursor()
        cursor.execute(sql)
        self.TyphoonText = cursor.fetchall()
        cursor.close()
        conn.close()
        return  self.TyphoonText

    def FilmSql(self):
        self.forecastType = self.FCT_cnToenDict[self.forecastType]
        self.sql = 'SELECT typhoonText FROM TYPHOON_TEXT WHERE initialTime LIKE "%s" and forecastType in ("%s");'%(self.initialTime,self.forecastType)
        return  self.sql

if __name__ == '__main__':
    time = "2018-01-01 00:00:00"
    fct = "英国全模"
    ty = TyphoonText(time,fct).SelectDB()
    print(ty)
