# _*_ encoding:utf-8 _*_
import sys,re
import codecs

from fliggy import Fliggy

reload(sys)

sys.setdefaultencoding('utf8')


def translateVec(vecs):
    res = []

    fg = Fliggy()
    translateVecfs = ''
    translateVecf = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\translateVec.txt', 'r', 'utf8')
    try:
        for line in translateVecf:
            translateVecfs += fg.fliggy(line[:line.find('\r')])
    finally:
        translateVecf.close()
    # print re.findall(u"136：", unicode(translateVecfs))
    for x in vecs.split(u","):
        single = re.findall(u"\D"+x+"：\D+", unicode(translateVecfs))[0]
        res.append(str(single[single.find(u"：")+1:]).strip())

    return ",".join(res)

# print translateVec(u"5,431")