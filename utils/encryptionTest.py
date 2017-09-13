# _*_ encoding:utf-8 _*_
import os
from fliggy import Fliggy


def scanDir(rootdir):
    """ 扫描整个目录下的文件

    :param rootdir: 要扫描的目录路径
    :return:
    """
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            yield filename


def read(fileName, rootdir, targetdir):
    """ 对源文件进行加密

    :param fileName: 要加密的源文件名
    :param rootdir: 源文件所在目录
    :param targetdir: 存放生成文件的目标目录
    :return:
    """
    try:
        f = open(rootdir+r'\\'+fileName, 'r')
        f_w = open(targetdir+r'\\'+fileName, 'w')
        fg = Fliggy()

        for line in f.readlines():
            line = line[:line.find('\r')]
            f_w.write(fg.encrypt(line)+'\n')
    finally:
        f.close()
        f_w.close()
    print 'end'


def encryption():
    """ 对某一文件夹下的所有文件进行加密
        rootdir：文件夹绝对路径
        targetdir：存放生成文件的目标目录
    :return:
    """
    rootdir = r"F:\wushijia\workspace\912\update"
    targetdir = r"C:\Users\admin\Desktop"
    for x in scanDir(rootdir):
        print x, read(x, rootdir, targetdir)


# encryption()
# read('pm.txt', r"F:\wushijia\workspace\medicineDialecticFilec", r"C:\Users\admin\Desktop")
