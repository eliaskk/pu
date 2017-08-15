# _*_ encoding:utf-8 _*_
import sys
import codecs

from medicineVec import read4Vec

reload(sys)

sys.setdefaultencoding('utf8')


def extractVec(filePath):
    """

    :param filePath: 读取的文本文件
    :return:
    """

    file = codecs.open(filePath, 'r', 'utf-8')
    outFile = filePath[:filePath.find(".txt")]+"_output"+filePath[filePath.find(".txt"):]
    f = open(outFile, 'w')
    try:
        for line in file:
            if line.startswith(u'主诉：'):

                f.writelines(str(','.join(read4Vec(line[line.find(u'主诉：')+3:])[0]))+' '+
                             str(','.join(read4Vec(line[line.find(u'主诉：')+3:])[1]))+'\n')
    finally:
        f.close()
        file.close()

filePath = u"F:\\wushijia\\workspace\\629\\皕一选方治验录629update.txt"
extractVec(filePath)
