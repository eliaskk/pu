# _*_ encoding:utf-8 _*_
import os
from fliggy import Fliggy


def scanDir():
    rootdir = r"F:\wushijia\workspace\814\update"
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            # print "parent is:" +parent
            # print "dirname is:"+dirname
            yield filename


def read(fileName):
    # fileName = 'dict3.txt'
    try:
        f = open(r'F:\wushijia\workspace\814\update\\'+fileName, 'r')
        f_w = open(r'C:\Users\admin\Desktop\\'+fileName, 'w')
        fg = Fliggy()

        for line in f.readlines():
            line = line[:line.find('\r')]
            # print fg.encrypt(line)
            # print fg.fliggy(line)
            # print fg.encrypt(line)
            print fg.encrypt(line)
            f_w.write(fg.encrypt(line)+'\n')
    finally:
        f.close()
        f_w.close()
    print 'end'


def encryption():
    for x in scanDir():
        # pass
        print x, read(x)

# encryption()
# read('pmfrom.txt')
