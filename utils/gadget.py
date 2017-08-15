# _*_ encoding:utf-8 _*_

import MySQLdb


def updatePrescriptionsReasonFromFile():
    pmfromF = open(r'F:\wushijia\workspace\84\pmfrom0804.txt', 'r')
    try:
        pmfrom = pmfromF.readlines()
    finally:
        pmfromF.close()
    conn = MySQLdb.connect("127.0.0.1", "root", "w1020392881", "candyonline", use_unicode=True, charset="utf8")
    cursor = conn.cursor()
    try:
        x = 0
        for line in pmfrom:
            x += 1
            line = line[:line.find('\n')]
            # print x, line
            sql = "update medicine_operation_test set prescriptionsReason='"+line+"' where id="+str(x)
            print cursor.execute(sql)
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# updatePrescriptionsReasonFromFile()
