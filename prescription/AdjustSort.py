# _*_ encoding:utf-8 _*_
"""
用方案二调整方案一排序
"""

from utils.fetchMedicine import *
from utils.findLineByWords import matchMedicineName
import re,codecs
from utils.findLineByVec import findNear


def adjustPrescriptionSort(originalSort,listin,threshold = 0.25):
    """
    :param originalSort: 方案一结果对应的pmfrom
    :param listin: 主诉
    :param threshold: 方案二阈值
    :return: 调整了排序的originalPrescriptionsSort 与 originalPrescriptionsReasonSort
    """
    if len(originalSort)>0:
        newList = []
        i = 0
        while i < len(originalSort):
            newList.append([originalSort[i],originalSort[i+1]])
            i += 2
        originalPrescriptionsReasonSort = originalSort[1:len(originalSort):2]
        matchMedicineList, listGroupDict = cmpMatchGroup(listin)
        if matchMedicineList[0][1] < threshold:
            return originalSort
        else:
            tempPrescription = matchMedicineList[0][0]
            counts = 0
            for eachPrescription in originalPrescriptionsReasonSort:
                if tempPrescription in matchMedicineName(re.split(u'\uff0c|\u3002',eachPrescription)[0]):
                    counts += 1
            if counts >= 1:
                newSort = sorted(newList,key=lambda x:tempPrescription in matchMedicineName(re.split(u'\uff0c|\u3002',x[1])[0]),reverse=True)
                newPrescriptionsSort = []
                for i in range(len(newSort)):
                    newPrescriptionsSort += newSort[i]
                return newPrescriptionsSort
            else:
                return originalSort
    else:
        return originalSort


def readSpecialGroupDict():
    """
    :return: specialGroupDict.txt  listSpecialGroupDict（list）：组合列表，dictMedicine（dict）以及药名优先级（数值大的优先级高）
    """
    listSpecialGroupDict = []
    listMedicine = []
    dictMedicine = {}
    ftext = codecs.open(r"F:\wushijia\workspace\medicineDialecticFilec\specialGroupDict.txt", "r", "utf8")
    try:
        fConfigText = ftext.readlines()
    finally:
        ftext.close()
    for eachText in fConfigText:
        eachText = eachText.strip('\r\n')
        eText = re.split(u"\uff1a|\u0020", eachText)
        listSpecialGroupDict.append([eText[0], re.split(u',', eText[1])])
        if eText[0] not in listMedicine:
            listMedicine.append(eText[0])
    for i in range(len(listMedicine)):
        dictMedicine.setdefault(listMedicine[i],len(listMedicine)-i)
    return dictMedicine,listSpecialGroupDict

def readWeight2mat(): #读取词向量权值
    # dictfile = codecs.open('F:\\weight2q.txt','r','utf-8')
    dict ={}
    dictfile = codecs.open(r'F:\wushijia\workspace\medicineDialecticFilec\weight2q.txt', 'r', 'utf-8')

    try:
        dictText = dictfile.readlines()
    finally:
        dictfile.close()
    for eachText in dictText:
        eachText = eachText.strip('\r\n')
        eText = eachText.split(' ')
        dict.setdefault(eText[0],eText[1])
    return dict

def compareMatchGroup(listin):
    """
    :param listin: 主诉对应的词向量列表
    :return: 与给定组合的匹配结果
                matchMedicineDict1（dict）：匹配到的药名为键，相应的权值和为值
                matchMedicineLists（list）：匹配到的药名按优先顺序排序后的列表
    """
    dictMedicine,listSpecialGroupDict = readSpecialGroupDict()
    weightDict = readWeight2mat()
    matchGroup = []#匹配上的药名与组合构成的二维list
    matchMedicine = []#匹配上的药名
    listin = findNear(listin)
    for item in listSpecialGroupDict:
        if set(item[1]).issubset(set(listin)):
            matchGroup.append(item)
            if item[0] not in matchMedicine:
                matchMedicine.append(item[0])
    if len(matchGroup) > 0:
        matchMedicineDict1 = {}#记录匹配到的相应权值和，以药名为键，以与该药名对应组合匹配上的组合的合并值为值
        matchMedicineDict2 = {}#记录匹配到的组合数，以药名对应的优先级序号为键，以与该药名匹配上的组合数个数为值
        for item in matchMedicine:
            matchMedicineDict1.setdefault(item,[])
            matchMedicineDict2.setdefault(dictMedicine[item],0)
        i = 0
        while i < len(matchMedicine):
            for eachMatchGroup in matchGroup:
                if matchMedicine[i] == eachMatchGroup[0]:
                    matchMedicineDict1[matchMedicine[i]] += eachMatchGroup[1]
                    matchMedicineDict2[dictMedicine[matchMedicine[i]]] += 1
            i += 1
        for key,value in matchMedicineDict1.items():
            value = list(set(value))
            tempWeight = 0
            for eachValue in value:
                tempWeight += int(weightDict[eachValue])
            matchMedicineDict1[key] = tempWeight
        matchMedicineList = sorted(matchMedicineDict2.items(),key=lambda item:(item[1],item[0]),reverse = True)
        matchMedicineLists = [list(dictMedicine.keys())[list(dictMedicine.values()).index(x[0])] for x in matchMedicineList]
        return matchMedicineDict1,matchMedicineLists
    else:
        return {},[]

def adjustPrescriptionSortTwo(originalSort,listRowRank,listin):
    """
    :param originalSort: 方案一返回结果排序
    :param listRowRank: 方案一匹配完后  行号与权值组成的排序
    :param listin: 主诉对应的向量
    :return: 方案一调整排序的结果，返回结果为list 【prescriptions,pmfrom,weight】
    """
    matchMedicineDict,matchMedicineList = compareMatchGroup(listin)
    prescription_1 = u"桂枝9克 芍药9克 甘草6克 生姜9克 大枣3枚"
    pmfrom_1 = u"桂枝汤，《伤寒论》条文：“太阳病，头痛发热，汗出恶风，桂枝汤主之。”--《伤寒论》"
    prescription_2 = u"麻黄9克 桂枝6克 甘草3克 杏仁6克"
    pmfrom_2 = u"麻黄汤， 《伤寒论》条文：“太阳病，脉浮紧无汗发热身疼痛，八九日不解，表证仍在，此当发其汗。服药已微除，其人发烦，目瞑，剧者必衄，衄乃解。所以然者，阳气重故也。麻黄汤主之。” --《伤寒论》"
    prescription_3 = u"葛根12克 麻黄9克 桂枝6克 生姜9克 甘草6克 芍药6克 大枣3枚"
    pmfrom_3 = u"葛根汤，《伤寒论》条文：“太阳病，项背强几几，无汗恶风，葛根汤主之。”--《伤寒论》"
    prescription_pmfrom = [[prescription_1,pmfrom_1],[prescription_2,pmfrom_2],[prescription_3,pmfrom_3]]
    if len(matchMedicineList) > 0: #匹配到specialGroupDict中的组合
        if len(originalSort)>0: #方案一返回结果不为空
            newList = []
            i = 0
            while i < len(originalSort):
                newList.append([originalSort[i], originalSort[i + 1],listRowRank[i+1][0]])
                i += 2
            originalPrescriptionsReasonSort = originalSort[1:len(originalSort):2]
            j = 0
            newPrescriptionsSort = []
            tempCountList = []
            while j < len(matchMedicineList):
                counts = 0
                for eachPrescription in originalPrescriptionsReasonSort:
                    if matchMedicineList[j][:-1] in re.split(u'\uff0c|\u3002',eachPrescription)[0]:
                        counts += 1
                tempCountList.append(counts)
                if counts >= 1:
                    newSort = sorted(newList,key=lambda x: matchMedicineList[j][:-1] in re.split(u'\uff0c|\u3002', x[1])[0],reverse=True)
                    for i in range(len(newSort)):
                        newPrescriptionsSort += newSort[i]
                    break
                else:
                    j += 1
            if tempCountList == [0 for x in range(len(tempCountList))]:#如果列表中的药方全部不在方案一中出现
                index = [f for f, items1 in enumerate(
                    [matchMedicineList[0] in re.split(u"\uff0c|\u3002", item1[1])[0] for item1 in prescription_pmfrom])
                         if items1 == True]
                tempSort = [prescription_pmfrom[index[0]]+[matchMedicineDict[matchMedicineList[0]]]]
                for j in range(len(newList)):
                    tempSort.append(newList[j])
                m = 0
                newSorts = []
                while m < 4 and m<len(tempSort):
                    newSorts += tempSort[m]
                return newSorts
            else:
                return newPrescriptionsSort
        else:#方案一返回结果为空
            newPrescriptionsSort = []
            m = 0
            for item in matchMedicineList:
                index = [f for f, items1 in enumerate([item in re.split(u"\uff0c|\u3002", item1[1])[0] for item1 in prescription_pmfrom]) if items1 == True]
                if m < 4:
                    m += 1
                    tempList = prescription_pmfrom[index[0]] + [matchMedicineDict[item]]
                    newPrescriptionsSort += tempList
                else:
                    break
            return newPrescriptionsSort
    else:
        if len(originalSort) > 0:  # 方案一返回结果不为空
            newList = []
            newPrescriptionsSort = []
            i = 0
            while i < len(originalSort):
                newList.append([originalSort[i], originalSort[i+1], listRowRank[i+1][0]])
                i += 2
            for item in newList:
                newPrescriptionsSort += item
            return newPrescriptionsSort
        else:
            return []


if __name__ == "__main__":
    listin = [9,33,12,14,152,410,1,80,255]#与三个汤分别匹配到两个组合   排序：桂枝>麻黄>葛根  [发热 汗出 恶风 脉缓 项强 身痛 无汗 脉浮】
#     listin = [9,33,12,14,152,410,1,80,255,136] #与葛根汤匹配到四个组合，其他两个汤分别匹配到两个组合 排序：葛根>桂枝>麻黄
    # listin = [9,33,12,152,410,1,80,255,136]   #麻黄两个，葛根两个，桂枝一个   排序：麻黄>葛根>桂枝
    # listin = [150,9,80,14,307]
    listin = [unicode(x) for x in listin]
    matchMedicineDict1, matchMedicineLists = compareMatchGroup(listin)
    for key,value in matchMedicineDict1.items():
        print "key = ",key,  "value = ",value
    for item in matchMedicineLists:
        print item
