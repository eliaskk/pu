# _*_ encoding:utf-8 _*_

import findLineByVec
import codecs
import re, sys

from fliggy import Fliggy

reload(sys)
sys.setdefaultencoding('utf-8')


def readPulseDict():
    """
    :return: 返回与脉象相关的词
    """
    listPulseDict = []
    fg = Fliggy()
    ftext = codecs.open(r"F:\wushijia\workspace\medicineDialecticFileAes\pulseDict.txt", "r", "utf8")
    try:
        fConfigText = ftext.readlines()
    finally:
        ftext.close()
    for eachText in fConfigText:
        eachText = fg.fliggy(eachText.strip('\r\n'))
        # eachText = eachText.strip('\r\n')
        # print eachText
        listPulseDict.append(eachText)
    return listPulseDict


def readGroupDict():
    """
    :return: listGroupDict(type：list )：对应groupDict.txt，listGroupDict每个元素的构成[药方 组合 组合概率]
            listMedicineName(type：list )：groupDict.txt里面所涉及到的药方列表
    """
    listGroupDict = []
    listMedicineName = []
    fg = Fliggy()
    # ftext = codecs.open(r"F:\wushijia\workspace\medicineDialecticFile\testGroupDict.txt", "r", "utf8")
    ftext = codecs.open(r"F:\wushijia\workspace\medicineDialecticFileAes\valueGroupDict.txt", "r", "utf8")

    try:
        fConfigText = ftext.readlines()
    finally:
        ftext.close()

    for eachText in fConfigText:
        eachText = unicode(fg.fliggy(eachText.strip('\r\n')))
        # eachText = fg.fliggy(eachText.strip('\r\n'))
        eText = re.split(u"\uff1a|\u0020", eachText)
        listGroupDict.append([eText[0], re.split(u',',eText[1]),float(eText[2])])  #listGroupDict每个元素的构成[药方 组合 组合概率]
        if eText[0] not in listMedicineName:
            listMedicineName.append(eText[0])
    return listGroupDict,listMedicineName


def fetchMatchGroup(listin):
    """
    :param listin: 主诉提取到的词向量集合
    :return:matchGroup(type:list)：listin与groupDict.txt匹配到的组合组成的list
            listMedicineNameDict（type：dict）：以groupDict.txt中涉及的药方为键值，并对每个键值赋值0
    """
    listPulseDict = readPulseDict()
    listGroupDict,listMedicineName = readGroupDict()
    matchGroup = []
    listin = findLineByVec.findNear(listin)             #将listin扩展，将listin里面的词的近义词也包含进来
    for k in range(len(listGroupDict)):
        if (set(listGroupDict[k][1])-set(listPulseDict)).issubset(set(listin)):
            matchGroup.append(listGroupDict[k])
    listMedicineNameDict = {}
    for eachText in listMedicineName:
        listMedicineNameDict.setdefault(eachText, 0)
    return listGroupDict,matchGroup,listMedicineNameDict


def cmpMatchGroup(listin):
    """
    :param listin: 主诉提取到的词
    :return:matchMedicineList(type:list):按药方对应的概率值从大到小排序
    """
    listGroupDict,matchGroup ,listMedicineNameDict= fetchMatchGroup(listin)
    for eachMatchGroup in matchGroup:
        tempMatchGroupName = eachMatchGroup[0]
        listMedicineNameDict[tempMatchGroupName] += eachMatchGroup[2]
    matchMedicineList = sorted(listMedicineNameDict.items(),key=lambda item:item[1],reverse=True)
    return matchMedicineList,listGroupDict


def fetchPrescriptionName(listin,threshold = 0.4):
    """
    :param listin: 主诉提取到的词向量集合
    :param threshold: 阈值
    :return: 1 计算结果如果大于阈值 则返回药方
         2 计算结果如果小于阈值 则返回频率值最大三个词向量或词向量组 （最多返回3个词向量）
          3 其他情况暂时返回false
    """
    matchMedicineList,listGroupDict = cmpMatchGroup(listin)
    if matchMedicineList[0][1] >= threshold:
        return matchMedicineList[0][0]  #直接返回药方
    else:
        topMatchMedicineList = [] #记录概率和大于0的药方
        intersectionList = []  # 每个元素的组成为[药方，组合，概率，组合与listin的交集与组合的差集]
        for i in range(len(matchMedicineList)):
            if matchMedicineList[i][1]>0:
                topMatchMedicineList.append(matchMedicineList[i])
            else:
                break
        if len(topMatchMedicineList) > 0:
            for i in range(len(topMatchMedicineList)):
                for j in range(len(listGroupDict)):
                    if topMatchMedicineList[i][0] == listGroupDict[j][0]:
                        tempIntersection = list(set(listin)&set(listGroupDict[j][1]))
                        if len(tempIntersection)>0 and len(tempIntersection)<len(listGroupDict[j][1]):
                            tempDiffSet = list(set(listGroupDict[j][1]) - set(tempIntersection))
                            tempList = listGroupDict[j]
                            tempList.append(tempDiffSet)
                            intersectionList.append(tempList)
            intersectionListSorted = sorted(intersectionList, key=lambda x: (len(x[-1]), x[2]),reverse=True)
            pushWordList = []
            tempWordList = []
            pushWordDict = {}
            n = 0
            while len(pushWordList) < 3 and n < len(intersectionListSorted):
                if set(intersectionListSorted[n][-1]) not in tempWordList:
                    pushWordList.append(intersectionListSorted[n][-1])
                    tempWordList.append(set(intersectionListSorted[n][-1]))
                n += 1
            for s in range(len(pushWordList)):
                pushWordDict.setdefault(tuple(pushWordList[s]),False)
            return pushWordDict     #小于阈值，最多返回频率靠前的三个
        else:
            return False            #其他情况，返回FALSE
        #排序：先按差集个数多的排，再按组合概率从大到小排

def pushWord(pushWordDict,listin,threshold = 0.4):
    """
    :param pushWord: 推荐给用户的词
    :param listin: 主诉提取到的词
    :param threshold: 阈值
    :return:
    """
    pushWords = []
    for key in pushWordDict:
        if pushWordDict[key] == True:
            pushWords += list(key)
    pushWords = list(set(pushWords))
    matchMedicineList, listGroupDict = cmpMatchGroup(listin)
    topMatchMedicineList = []  # 记录概率和大于0的药方
    intersectionList = []  # 每个元素的组成为[药方，组合，概率，组合与listin的交集与组合的差集]
    for i in range(len(matchMedicineList)):
        if matchMedicineList[i][1] > 0:
            topMatchMedicineList.append(matchMedicineList[i])
        else:
            break
    topMatchMedicineDict = {}
    for i in range(len(topMatchMedicineList)):
        topMatchMedicineDict.setdefault(topMatchMedicineList[i][0], topMatchMedicineList[i][1])
    if len(topMatchMedicineList) > 0:
        for i in range(len(topMatchMedicineList)):
            for j in range(len(listGroupDict)):
                if topMatchMedicineList[i][0] == listGroupDict[j][0]:
                    tempIntersection = list(set(listin) & set(listGroupDict[j][1]))
                    if len(tempIntersection) < len(listGroupDict[j][1]):
                        tempDiffSet = list(set(listGroupDict[j][1]) - set(tempIntersection))
                        tempList = listGroupDict[j]
                        tempList.append(tempDiffSet)
                        intersectionList.append(tempList)
    intersectionListSorted = sorted(intersectionList, key=lambda x: (len(x[-1]), x[2]), reverse=True)
    tempTopMatchMedicineDict = topMatchMedicineDict
    m = len(intersectionListSorted)
    for j in range(m):
        tempVec = findLineByVec.findNear(pushWords)
        if set(intersectionListSorted[j][-1]).issubset(set(tempVec)):
            tempTopMatchMedicineDict[intersectionListSorted[j][0]] += intersectionListSorted[j][2]
    tempResult = sorted(tempTopMatchMedicineDict.items(), key=lambda item: item[1], reverse=True)
    if tempResult[0][1] >= threshold:
        return tempResult[0][0]
    else:
        return False


if __name__ == "__main__":
    # u'肚子痛，小便不通，背拘急，腿痛，拉肚子，发烧，脉细，无汗'
    listin = u'36,52,143,33'
    listin = listin.split(u',')
    # print fetchPrescriptionName(listin, threshold=0.25)








