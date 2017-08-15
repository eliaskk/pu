# _*_ encoding:utf-8 _*_

import codecs, MySQLdb
import sys
import re

from medicineVec import strlineWord2par2, strlineWord2par3, strlineWord2par4

reload(sys)

sys.setdefaultencoding('utf8')


def generatorLineByFile(pmtotals, strs, n):
    for line in pmtotals:
        line = unicode(line)
        n += 1
        if line.startswith(u"主诉："):
            if len(strs) == 2:
                if strlineWord2par2(line.encode("utf-8"), strs[0].encode("utf-8"), strs[1].encode("utf-8")):
                    yield n
            elif len(strs) == 3:
                if strlineWord2par3(line.encode("utf-8"), strs[0].encode("utf-8"), strs[1].encode("utf-8"), strs[2].encode("utf-8")):
                    yield n
            elif len(strs) == 4:
                if strlineWord2par4(line.encode("utf-8"), strs[0].encode("utf-8"), strs[1].encode("utf-8"), strs[2].encode("utf-8"), strs[3].encode("utf-8")):
                    yield n
    return


def findKeyFromPatientContentByFile(strs):
    pmtotal = codecs.open(r'F:\wushijia\workspace\727\pmtotall0727.txt', 'r', 'utf8')
    pmtotals = pmtotal.readlines()
    pmtotal.close()
    return generatorLineByFile(pmtotals, strs, 0)


def generatorLineByDB(pmtotals, strs, n):
    for x in pmtotals:
        n += 1
        if len(strs) == 2:
            if strlineWord2par2(x[1].encode("utf-8"), strs[0].encode("utf-8"), strs[1].encode("utf-8")):
                yield n
        elif len(strs) == 3:
            if strlineWord2par3(x[1].encode("utf-8"), strs[0].encode("utf-8"), strs[1].encode("utf-8"),
                                strs[2].encode("utf-8")):
                yield n
        elif len(strs) == 4:
            if strlineWord2par4(x[1].encode("utf-8"), strs[0].encode("utf-8"), strs[1].encode("utf-8"),
                                strs[2].encode("utf-8"), strs[3].encode("utf-8")):
                yield n
    return


def findKeyFromPatientContentByDB(strs, start, end):
    conn = MySQLdb.connect("127.0.0.1", "root", "w1020392881", "candyonline", use_unicode=True, charset="utf8")
    cursor = conn.cursor()
    try:
        sql = "SELECT id,patientContent FROM medicine_operation WHERE id BETWEEN "+start+" AND "+end
        cursor.execute(sql)
        rs = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return generatorLineByDB(rs, strs, int(start))


def generatorLineByArgs(strs, start=-1, end=-1):
    """ 查找主诉中是否包含某个字符串，并返回所在行

    :param strs:
    :param start:
    :param end:
    :return:
    """
    rs = []
    if start is -1 and end is -1:
        rs = findKeyFromPatientContentByFile(strs)
    else:
        rs = findKeyFromPatientContentByDB(strs, str(start), str(end))
    for x in rs:
        print x
    return rs


def matchMedicineName(strs):
    """ 根据字符串匹配经方向量组中相应的经方
        文件medicineVec.txt即是经方向量组.txt
    :param strs:
    :return:
    """
    res = []
    tmps_medicine = ""
    # medicineVec = open(r"F:\wushijia\workspace\713\specialMedicine.txt", "r")
    medicineVec = codecs.open(r"F:\wushijia\workspace\medicineDialecticFilec\specialMedicine.txt", "r","utf-8")

    medicineVecs = medicineVec.readlines()
    medicineVec.close()
    allItems = re.split(u'\u5408|\uff0c',strs)
    for str in allItems:
        for line in medicineVecs:
            # line = unicode(line)
            # line = line[:line.find(u"\r\n")]
            line = line.strip('\r\n')
            if (u'汤' in str) and (u'加' in str) and (str.index(u'汤') < str.index(u'加')):
                str = str[:str.find(u'加')]
                if len(re.compile(u"汤").findall(str)) > 1:
                    if line in str:
                        res.append(line)
                    if len(list(set(line).intersection(set(str)))) == len(line):
                        if len(line) > len(tmps_medicine):
                            tmps_medicine = line
                elif line == str:
                    tmps_medicine = line
                    res.append(line)
                elif len(line) == len(str):
                    if len(list(set(line).intersection(set(str)))) == len(line) and len(
                            list(set(line).intersection(set(str)))) == len(str):
                        tmps_medicine = line
                        res.append(line)
                elif len(line) > len(str) or len(str) > len(line):
                    if len(list(set(line).intersection(set(str)))) == len(line):
                        if len(line) > len(tmps_medicine):
                            tmps_medicine = line
            else:
                if len(re.compile(u"汤").findall(str)) > 1:
                    if line in str:
                        res.append(line)
                    if len(list(set(line).intersection(set(str)))) == len(line):
                        if len(line) > len(tmps_medicine):
                            tmps_medicine = line
                elif line == str:
                    tmps_medicine = line
                    res.append(line)
                elif len(line) == len(str):
                    if len(list(set(line).intersection(set(str)))) == len(line) and len(
                            list(set(line).intersection(set(str)))) == len(str):
                        tmps_medicine = line
                        res.append(line)
                elif len(line) > len(str) or len(str) > len(line):
                    if len(list(set(line).intersection(set(str)))) == len(line):
                        if len(line) > len(tmps_medicine):
                            tmps_medicine = line

        if tmps_medicine != "":
            res.append(tmps_medicine)

        tmps_medicine = ""
    res = list(set(res))

    # for x in res:
    #     print x
    return res

matchMedicineName(u"麻杏石甘汤合栀子柏皮汤合桔梗甘草汤")