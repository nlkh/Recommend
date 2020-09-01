import pymysql
db_connect = pymysql.connect(
    user='root',
    passwd='',
    host='127.0.0.1',
    db='ngn',
    charset='utf8'
)
cursor = db_connect.cursor(pymysql.cursors.DictCursor)