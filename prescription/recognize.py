# _*_ encoding:utf-8 _*_
import re, MySQLdb


def command_toast(text):
    return text.encode('gbk', 'ignore')


def transcoding(field):
    if not isinstance(field, unicode):
        return unicode(field, "gbk", "ignore")
    else:
        return field


def single():
    fileName = r'F:\wushijia\workspace\527\prescriptions2.txt'
    f = open(fileName, 'r')
    prescriptions = []
    for line in f:
        content = unicode(line, 'utf-8')
        print isinstance(content, unicode)
        prescription = content[content.find(u'：') + 1:content.find(u'\n')]
        for x in re.split(u'，|/|\\n', prescription):
            if x not in prescriptions:
                print x
                prescriptions.append(x)

    # print len(prescriptions)
    # print '------------------------------------------'
    host = "127.0.0.1"

    user = "root"

    pwd = "w1020392881"

    db = "candyonline"

    db = MySQLdb.connect(host, user, pwd, db, use_unicode=True, charset="utf8")
    try:
        cursor = db.cursor()
        for x in prescriptions:
            sql = "insert into single(singleMedicine) VALUES ('" + x + "')"
            print cursor.execute(sql)
        db.commit()
    except Exception, e:
        print e.message
    finally:
        db.rollback()
        cursor.close()
        db.close()


def savePrescriptions():
    """
    按照药名：药方插入数据库
    :return:
    """
    fileName = r'F:\wushijia\workspace\527\prescriptions2.txt'
    f = open(fileName, 'r')
    prescriptionNames = []
    prescriptions = []
    for line in f:
        content = unicode(line, 'utf-8')
        prescriptionNames.append(content[0:content.find(u'：')])
        prescriptions.append(content[content.find(u'：')+1:])

    host = "127.0.0.1"

    user = "root"

    pwd = "w1020392881"

    db = "candyonline"

    db = MySQLdb.connect(host, user, pwd, db, use_unicode=True, charset="utf8")
    try:
        cursor = db.cursor()
        sql = "insert into prescriptions(prescriptionsName,prescriptions) VALUES (%s,%s)"
        lis = []
        for x in range(len(prescriptionNames)):
            data = (prescriptionNames[x], prescriptions[x])
            lis.append(data)
            print cursor.executemany(sql, lis)
            del lis[:]
        db.commit()
    except Exception, e:
        print e.message
    finally:
        db.rollback()
        cursor.close()
        db.close()


def recoginze():
    input = transcoding(raw_input(command_toast(u"请输入表名药方组合，药方之间用中文逗号隔开：")))
    f = ''
    host = "127.0.0.1"

    user = "root"

    pwd = "w1020392881"

    db = "candyonline"

    db = MySQLdb.connect(host, user, pwd, db, use_unicode=True, charset="utf8")

    sql = "select singleMedicine from single"
    cursor = db.cursor()
    cursor.execute(sql)
    rs = cursor.fetchall()
    cursor.execute("select * from prescription")
    f = cursor.fetchall()
    cursor.close()
    db.close()

    singles = input.split(u'，')

    for k in range(len(singles)):
        for j in rs:
            if singles[k].find(j[0]) is not -1:
                singles[k] = j[0]

    index = []
    res = []

    for line in f:
        # print line[1] 药名
        # print line[2] 药方
        prescription2 = re.split(u'，|/|\\n', line[2])
        tmp = list(set(prescription2).intersection(set(singles)))
        index.append(len(tmp))

    for x in range(len(index)):
        # 如果集合中某个数是该集合最大的数，记下该数在数列中的位置
        if index[x] == max(index):
            res.append(x)

    print u"\n药名："
    for x in res:
        print f[x][1]

recoginze()
# savePrescriptions()