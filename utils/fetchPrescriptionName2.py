# _*_ encoding:utf-8 _*_

import sys

reload(sys)

sys.setdefaultencoding('utf8')


def genertorLine(vec):
    lis = vec.split(u',')
    groupDict = open(r'F:\wushijia\workspace\710\testGroupDict.txt', 'r')
    groupDicts = groupDict.readlines()
    groupDict.close()
    n = 0
    for line in groupDicts:
        n += 1
        line = unicode(line)
        nums = line[line.find(u"：")+1:line.find(u"\n")]
        line_lis = nums[:nums.find(u"：")]
        if len(list(set(lis).intersection(set(line_lis.split(u","))))) == len(line_lis.split(u",")):
            yield line


def fetchPrescriptionName(strs):
    prescriptionNames = []
    for x in genertorLine(strs):
        if x[:x.find(u"：")] not in prescriptionNames:
            prescriptionNames.append(x[:x.find(u"：")])
    for x in prescriptionNames:
        print x

strs = u"27,40,188,28,9,247"
fetchPrescriptionName(strs)
