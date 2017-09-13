# _*_ encoding:utf-8 _*_

import codecs, MySQLdb
import sys
import re
from fliggy import Fliggy

from medicineVec import strlineWord2par2, strlineWord2par3, strlineWord2par4

reload(sys)

sys.setdefaultencoding('utf8')


def matchMedicineName(strs):
    """ 根据字符串匹配经方向量组中相应的经方
        文件medicineVec.txt即是经方向量组.txt
    :param strs:
    :return:
    """
    res = []

    fg = Fliggy()
    tmps_medicine = ""
    # medicineVec = open(r"F:\wushijia\workspace\713\specialMedicine.txt", "r")
    medicineVec = codecs.open(r"F:\wushijia\workspace\medicineDialecticFileAes\specialMedicine.txt", "r","utf-8")

    medicineVecs = medicineVec.readlines()
    medicineVec.close()
    allItems = re.split(u'\u5408|\uff0c',strs)
    for str in allItems:
        for line in medicineVecs:
            # line = unicode(line)
            # line = line[:line.find(u"\r\n")]
            line = fg.fliggy(line.strip('\r\n'))
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