# _*_ encoding:utf-8 _*_
import sys
import codecs
import MySQLdb

reload(sys)

sys.setdefaultencoding('utf8')


def readMedicineName():
    f = codecs.open(r'F:\wushijia\workspace\623\medicineName.txt', 'r', 'utf-8')
    try:
        medicineName = f.readlines()
    finally:
        f.close()
    lis = []
    sql = "insert into classicmedicine(medicineName,medicineCompose) VALUES (%s,%s)"
    conn = MySQLdb.connect("127.0.0.1", "root", "w1020392881", "candyonline", use_unicode=True, charset="utf8")
    cursor = conn.cursor()
    try:
        for line in medicineName:
            medicneName = line[line.find(u' ')+1:line.find(u'：')]
            medicine = line[line.find(u'：')+1:line.find(u'\r')]
            data = (medicneName, medicine)
            lis.append(data)
            print cursor.executemany(sql, lis)
            del lis[:]
    finally:
        conn.commit()
        cursor.close()
        conn.close()


# readMedicineName()