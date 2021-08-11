import pymysql
def MysqlConnectFun(TableName):
    db_connect = pymysql.connect(host='10.28.16.202', port=3306, user='root', passwd='daohang507', db='cmrcreportsystem',
                             charset='utf8')
