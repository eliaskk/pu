# _*_ encoding:utf-8 _*_
import re, codecs

from fliggy import Fliggy


def findNear(lis):
    res = []
    nearVec = codecs.open(r"F:\wushijia\workspace\medicineDialecticFilec\nearVec.txt", "r", "utf8")
    nearVecs = nearVec.read()
    nearVec.close()
    for x in lis:
        res += re.findall('\d+', ''.join(re.findall('\D+' + x + ' \d+', nearVecs)))
    res += lis
    res = list(set(res))
    return res


def read(lis, f):
    n = 0
    for line in f:
        n += 1
        line = line[:line.find(u'\n')]
        if len(list(set(findNear(unicode(line))).intersection(set(lis.split(u','))))) == len(lis.split(u',')):
            m = yield n
    return


def write(lis):
    # fileName = r'F:\pm.txt'
    fileName = r'F:\wushijia\workspace\medicineDialecticFilec\pm.txt'
    f = open(fileName, 'r')
    outName = fileName[:fileName.find('.txt')]
    outName += lis.replace(u',', u'_') + "_output.txt"
    outFile = open(outName, 'w')
    # read(lis, f)
    for x in read(lis, f):
        outFile.write(str(x)+"\n")
    outFile.close()
    f.close()
    return outName

def write2(lis):
    res = []
    fileName = r'F:\wushijia\workspace\medicineDialecticFilec\pm.txt'
    f = open(fileName, 'r')
    for x in read(lis, f):
        res.append(x)
    return res

# write(u"152,80")
# print write2(u"152,80")



