# coding=utf-8

import os
import sys
import re
import codecs
import json

from utils.fliggy import Fliggy
from AdjustSort import adjustPrescriptionSort
from medicineVec import read4Vec


reload(sys)
sys.setdefaultencoding('utf-8')


def strlineWord2par2(str, uPar1, uPar2):
    ret = re.split(u'\uff0c|\u3002|\u3001|ff01', str)
    ti = 0
    while ti < len(ret):
        retone = re.search(uPar1, ret[ti])
        if retone:
            rettwo = re.search(uPar2, ret[ti][ret[ti].index(uPar1):])
            if rettwo:

                break
            else:
                ti += 1
        else:
            ti += 1
    if ti >= len(ret):
        return False
    else:
        return True


def strlineWord2par3(str, uPar1, uPar2, uPar3):
    ret = re.split(u'\uff0c|\u3002|\u3001|ff01', str)
    ti = 0
    while ti < len(ret):
        retone = re.search(uPar1, ret[ti])
        if retone:
            rettwo = re.search(uPar2, ret[ti][ret[ti].index(uPar1):])
            if rettwo:
                retthree = re.search(uPar3, ret[ti][ret[ti].index(uPar2):])
                if retthree:
                    break
                else:
                    ti += 1
            else:
                ti += 1
        else:
            ti += 1

    if ti >= len(ret):
        return False
    else:
        return True


def strlineWord2par4(str, uPar1, uPar2, uPar3, uPar4):
    ret = re.split(u'\uff0c|\u3002|\u3001|ff01', str)
    ti = 0
    while ti < len(ret):
        retone = re.search(uPar1, ret[ti])
        if retone:
            rettwo = re.search(uPar2, ret[ti][ret[ti].index(uPar1):])
            if rettwo:
                retthree = re.search(uPar3, ret[ti][ret[ti].index(uPar2):])
                if retthree:
                    retfour = re.search(uPar4, ret[ti][ret[ti].index(uPar3):])
                    if retfour:
                        break
                    else:
                        ti += 1
                else:
                    ti += 1
            else:
                ti += 1
        else:
            ti += 1

    if ti >= len(ret):
        return False
    else:
        return True


def strwordVec2Serialize(str, listin, listout, count):
    listinLen = len(listin)
    i = 0
    if count == 3:
        while (count * i) < listinLen:
            if strlineWord2par2(str, listin[count * i + 1], listin[count * i + 2]) == True:
                listout.append(listin[count * i])
            i += 1
    elif count == 4:
        while (count * i) < listinLen:
            if strlineWord2par3(str, listin[count * i + 1], listin[count * i + 2], listin[count * i + 3]) == True:
                listout.append(listin[count * i])
            i += 1
    elif count == 5:
        while (count * i) < listinLen:
            if strlineWord2par4(str, listin[count * i + 1], listin[count * i + 2], listin[count * i + 3],
                                listin[count * i + 4]) == True:
                listout.append(listin[count * i])
            i += 1


def cmpSplit(strsplit, cmpElement):
    str = strsplit.split(',')
    strLen = len(str)
    i = 0

    while i < strLen:

        tem = int(str[i])
        if tem == cmpElement:
            break
        else:
            i += 1

    if i >= strLen:
        return False
    else:
        return True


def mat4Sympthom(str, strLen, listin, listinLen, dict, listout):
    j = 0
    while j < strLen:
        i = 0
        while i < listinLen:
            tem = int(listin[i])
            if cmpSplit(str[j], tem) == True:
                weight = dict.get(listin[i])
                weightInt = int(weight)
                listout[j][i] = 1 * weightInt
                i += 1
            else:
                listout[j][i] = 0
                i += 1
        j += 1


def rank4Symptom(listin, cols, rows, listout):
    j = 0
    while j < rows:
        i = 0
        sum = 0
        while i < cols:
            sum += listin[j][i]
            if sum > 4 and not j in listout:
                listout.append(j)
                i += 1
            else:
                i += 1
        j += 1


def cmpList(listone, listtwo, listrows, listout):
    i = 0
    listLen = len(listone)
    listtem = []
    for eachitem in listone:
        listtem.append(eachitem)

    for item in listtwo:
        while i < listLen:
            if item == listtem[i]:
                listout.append(listrows[i])
                listtem[i] = 0
                i = 0
                break
            else:
                i += 1


def find4TopDict(listin):
    listtopSort = []
    listRows = []
    listRowsSorted = []
    listRows.append(listin[1])
    listRows.append(listin[3])
    listRows.append(listin[5])
    listRows.append(listin[7])
    listRows.append(listin[9])
    listtopSort.append(listin[0])
    listtopSort.append(listin[2])
    listtopSort.append(listin[4])
    listtopSort.append(listin[6])
    listtopSort.append(listin[8])

    listtopSorted = sorted(listtopSort, key=lambda x: (x[0], x[1]))

    listtopSortedReverse = sorted(listtopSort, key=lambda x: (x[0], x[1]), reverse=True)

    cmpList(listtopSort, listtopSortedReverse, listRows, listRowsSorted)
    listin[0] = listtopSortedReverse[0]
    listin[2] = listtopSortedReverse[1]
    listin[4] = listtopSortedReverse[2]
    listin[6] = listtopSortedReverse[3]
    listin[1] = listRowsSorted[0]
    listin[3] = listRowsSorted[1]
    listin[5] = listRowsSorted[2]
    listin[7] = listRowsSorted[3]
    listin[8] = [0, listin[8][1]]
    listin[9] = 0


def sort4Precription(listin, cols, rows, listout, listrow):
    j = 0
    sumnum = [0, 4]
    topone = [1, 3]
    toptwo = [2, 2]
    topthree = [3, 1]
    topfour = [3, 0]
    toponerow = 0
    toptworow = 0
    topthreerow = 0
    topfourrow = 0
    sumrow = 0
    listtoptotall = [topone, toponerow, toptwo, toptworow, topthree, topthreerow, topfour, topfourrow, sumnum, sumrow]

    while j < rows:
        i = 0
        while i < cols:
            listtoptotall[8] = [listtoptotall[8][0] + listin[j][i], j + 5]
            listtoptotall[9] = j
            i += 1
        find4TopDict(listtoptotall)
        j += 1

    listout.append(listtoptotall[1])
    listout.append(listtoptotall[0])
    listout.append(listtoptotall[3])
    listout.append(listtoptotall[2])
    listout.append(listtoptotall[5])
    listout.append(listtoptotall[4])
    listout.append(listtoptotall[7])
    listout.append(listtoptotall[6])

    listrow.append(listtoptotall[1])
    listrow.append(listtoptotall[3])
    listrow.append(listtoptotall[5])
    listrow.append(listtoptotall[7])


def readDict2list(allftext, listout):
    listWordVec2 = []
    listWordVec3 = []
    listWordVec4 = []
    listSerout2 = []
    listSerout3 = []
    listSerout4 = []

    fg = Fliggy()
    fdict2 = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\dict2.txt', 'r', 'utf-8')
    fdict3 = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\dict3.txt', 'r', 'utf-8')
    fdict4 = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\dict4.txt', 'r', 'utf-8')
    try:
        fdict2Text = fdict2.readlines()
        fdict3Text = fdict3.readlines()
        fdict4Text = fdict4.readlines()
    finally:
        fdict2.close()
        fdict3.close()
        fdict4.close()

    for eachText in fdict2Text:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        eText = unicode(eachText).split(' ')
        listWordVec2.append(eText[0])
        listWordVec2.append(eText[1])
        listWordVec2.append(eText[2])

    # print "----listWordVec2-----"
    # print listWordVec2[3]
    # print fdict2Text[3]

    for eachText in fdict3Text:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        eText = eachText.split(' ')
        listWordVec3.append(eText[0])
        listWordVec3.append(eText[1])
        listWordVec3.append(eText[2])
        listWordVec3.append(eText[3])

    for eachText in fdict4Text:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        eText = eachText.split(' ')
        listWordVec4.append(eText[0])
        listWordVec4.append(eText[1])
        listWordVec4.append(eText[2])
        listWordVec4.append(eText[3])
        listWordVec4.append(eText[4])

    strwordVec2Serialize(allftext, listWordVec2, listSerout2, 3)
    strwordVec2Serialize(allftext, listWordVec3, listSerout3, 4)
    strwordVec2Serialize(allftext, listWordVec4, listSerout4, 5)

    for item in listSerout2:
        listout.append(item)

    for item in listSerout3:
        listout.append(item)

    for item in listSerout4:
        listout.append(item)


def strreadDict2list(allftext, listout):
    listWordVec2 = []
    listWordVec3 = []
    listWordVec4 = []
    listSerout2 = []
    listSerout3 = []
    listSerout4 = []

    fg = Fliggy()
    fdict2 = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\dict2.txt', 'r', 'utf-8')
    fdict3 = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\dict3.txt', 'r', 'utf-8')
    fdict4 = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\dict4.txt', 'r', 'utf-8')
    try:
        fdict2Text = fdict2.readlines()
        fdict3Text = fdict3.readlines()
        fdict4Text = fdict4.readlines()
    finally:
        fdict2.close()
        fdict3.close()
        fdict4.close()

    for eachText in fdict2Text:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        eText = unicode(eachText).split(' ')
        listWordVec2.append(eText[0])
        listWordVec2.append(eText[1])
        listWordVec2.append(eText[2])

    for eachText in fdict3Text:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        eText = eachText.split(' ')
        listWordVec3.append(eText[0])
        listWordVec3.append(eText[1])
        listWordVec3.append(eText[2])
        listWordVec3.append(eText[3])

    for eachText in fdict4Text:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        eText = eachText.split(' ')
        listWordVec4.append(eText[0])
        listWordVec4.append(eText[1])
        listWordVec4.append(eText[2])
        listWordVec4.append(eText[3])
        listWordVec4.append(eText[4])

    strwordVec2Serialize(allftext, listWordVec2, listSerout2, 3)
    strwordVec2Serialize(allftext, listWordVec3, listSerout3, 4)
    strwordVec2Serialize(allftext, listWordVec4, listSerout4, 5)

    for item in listSerout2:
        listout.append(item)

    for item in listSerout3:
        listout.append(item)

    for item in listSerout4:
        listout.append(item)


def vecConflict(listin):
    listpos = []
    listneg = []
    fg = Fliggy()
    fcon = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\vecconflict.txt', 'r', 'utf-8')
    try:
        vecText = fcon.readlines()
    finally:
        fcon.close()
    for eachText in vecText:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        eText = eachText.split(' ')
        listpos.append(eText[0])
        listneg.append(eText[1])

    i = 0
    while i < len(listpos):
        if listpos[i] in listin and listneg[i] in listin:
            listin.remove(listneg[i])
        i += 1


def readWeight2mat(dict):
    dictfile = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\weight2q.txt', 'r', 'utf-8')
    fg = Fliggy()
    try:
        dictText = dictfile.readlines()
    finally:
        dictfile.close()
    for eachText in dictText:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        eText = eachText.split(' ')
        dict.setdefault(eText[0], eText[1])


def readPrecriptions2mat(listin):
    file = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\prescriptions.txt', 'r', 'utf-8')
    try:
        fileText = file.readlines()
    finally:
        file.close()
    fg = Fliggy()
    for eachText in fileText:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        listin.append(unicode(eachText))
    return listin


def readSheetFormat(dict):
    file = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\liujinsheetformat.txt', 'r', 'utf-8')
    try:
        fileText = file.readlines()
    finally:
        file.close()

    fg = Fliggy()
    for eachText in fileText:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        eText = eachText.split(' ')
        dict.setdefault(eText[0], eText[1])

        # print "readSheetFormat"
        # print dict


def readFilter(listout):
    file = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\filter.txt', 'r', 'utf-8')
    try:
        fileText = file.readlines()
    finally:
        file.close()
    # print "------readFilter-----"
    fg = Fliggy()
    for eachText in fileText:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        # print eachText
        listout.append(eachText)


def rank4Precription2(listpre, listrow, listout):
    whichrow = len(listrow)
    i = 0
    while i < whichrow:
        if listrow[i + 1][0] <= 4:
            break
        else:
            listout.append(listpre[listrow[i]])
        i += 2


def rank4Precription3(listpre, listrow, listout, listpmfrom):
    whichrow = len(listrow)
    i = 0
    while i < whichrow:
        if listrow[i + 1][0] <= 4:
            break
        else:
            listout.append(listpre[listrow[i]])
            listout.append(listpmfrom[listrow[i]])
        i += 2



def findSheeteach(strin, dict, filterList, lenfilter, listout):
    eText = strin.split(u'\u3002')
    leneText = len(eText)
    i = 0
    listtem = []
    while i < lenfilter:
        j = 0
        while j < leneText:
            temInt = int(dict.get(filterList[i]))
            if temInt == 1:
                if eText[j].find(filterList[i]) != -1:
                    tem = eText[j].split(u'\uff1a')
                    strreadDict2list(tem[1], listtem)
                    j += 1
                else:
                    j += 1
            else:
                j += 1
        i += 1

    for item in listtem:
        listout.append(item)


def read4Pmfrom(listin):
    fromfile = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\pmfrom.txt', 'r', 'utf-8')
    try:
        fileText = fromfile.readlines()
    finally:
        fromfile.close()

    fg = Fliggy()
    for eachText in fileText:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        listin.append(unicode(eachText))
    return listin


def rank4Medicine(patientSay, patientSheet):
    ff = codecs.open(r'F:\wushijia\workspace\medicineDialecticFileAes\pm.txt', 'r', 'utf-8')
    # ff = codecs.open(r'F:\wushijia\workspace\medicineDialecticFilec\pm.txt', 'r', 'utf-8')
    fg = Fliggy()
    try:
        allText = []
        for line in ff.readlines():
            line = line[:line.find('\r')]
            # print unicode(fg.fliggy(line))
            allText.append(unicode(fg.fliggy(line)))
            # allText.append(line)
        # print allText
        # print ff.readlines()
        # allText = fg.fliggy(allText)
        lenallText = len(allText)
    finally:
        ff.close()

    allftext = patientSay
    sheetText = patientSheet

    listRank = []
    dictWeight2mat = {}
    listRowRank = []
    listwordvec = []
    listPrescription = []
    listRows = []
    listRankPre = []
    dictSheetFormat = {}
    listFilter = []
    listSheetVec = []
    listPmfrom = []

    readSheetFormat(dictSheetFormat)
    # print "-----readSheetFormat-------"
    # print dictSheetFormat
    readFilter(listFilter)
    # print "-----listFilter------"
    # print listFilter
    findSheeteach(sheetText, dictSheetFormat, listFilter, 9, listSheetVec)

    listSheetVeced = list(set(listSheetVec))
    listSheetVeced.sort(key=listSheetVec.index)
    # print "----listSheetVeced-----"
    # print listSheetVeced

    readDict2list(allftext, listwordvec)
    vecConflict(listwordvec)

    for item in listSheetVeced:
        listwordvec.append(item)

    listwordveced = list(set(listwordvec))
    listwordveced.sort(key=listwordvec.index)
    len4Serlist = len(listwordveced)
    # print listwordveced

    readWeight2mat(dictWeight2mat)
    list2d = [[0 for col in range(len4Serlist)] for row in range(lenallText)]
    mat4Sympthom(allText, lenallText, listwordveced, len4Serlist, dictWeight2mat, list2d)
    sort4Precription(list2d, len4Serlist, lenallText, listRowRank, listRows)
    readPrecriptions2mat(listPrescription)
    read4Pmfrom(listPmfrom)

    rank4Precription3(listPrescription, listRowRank, listRankPre, listPmfrom)
    listRankSorts = adjustPrescriptionSort(listRankPre, read4Vec(allftext)[0], threshold=0.25)

    # return listRankPre
    return listRankSorts




