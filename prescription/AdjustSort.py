# _*_ encoding:utf-8 _*_

from utils.fetchMedicine import *
from utils.findLineByWords import matchMedicineName

def adjustPrescriptionSort(originalSort,listin,threshold = 0.25):
    """
    :param originalPrescriptionsSort: 方案一结果对应的prescriptions
    :param originalPrescriptionsReasonSort: 方案一结果对应的pmfrom
    :param listin: 主诉
    :param threshold: 方案二阈值
    :return: 调整了排序的originalPrescriptionsSort 与 originalPrescriptionsReasonSort
    """
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




if __name__ == "__main__":
    originalPrescriptionReasonSort = [u'桂枝9克 白芍9克 生姜9克 大枣4枚 炙甘草6克',u'桂枝加芍药汤合真武汤，桂枝汤证。--经方传真',u'桂枝12克 白芍9克 生姜10克 大枣4枚 炙甘草6克',u'桂枝加芍药汤，桂枝加芍药、饴糖即小建中汤，加饴糖更加重缓中止痛的作用。有的药房无饴糖。--经方传真',u'桂枝15克 白芍10克 生姜10克 大枣4枚 炙甘草6克',u'桂枝加葛根汤，伤寒论12条：太阳病，项背强几几，反汗出恶风者，桂枝加葛根汤主之。--经方传真',u'大枣4枚 炙甘草6克',u'桂枝加芍药汤加味，胃炎（门纯德医案）--皕一选方治验录']
    # originalPrescriptionsSort = [u'桂枝9克 白芍9克 生姜9克 大枣4枚 炙甘草6克',u'桂枝12克 白芍9克 生姜10克 大枣4枚 炙甘草6克',u'桂枝15克 白芍10克 生姜10克 大枣4枚 炙甘草6克',u'大枣4枚 炙甘草6克']
    for item in originalPrescriptionReasonSort:
        print item
    listin = [u'27',u'192']
    aa = adjustPrescriptionSort(originalPrescriptionReasonSort,listin,0.25)
    for item in aa:
         print item