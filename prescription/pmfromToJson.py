# _*_ encoding:utf-8 _*_

import sys, re
import json

from utils.fliggy import Fliggy

# reload(sys)
#
# sys.setdefaultencoding('utf8')


def pmfromToJson():

    fg = Fliggy()

    pmfromf = open(r'F:\wushijia\workspace\medicineDialecticFileAes\pmfrom.txt', 'r')
    prescriptionsf = open(r'F:\wushijia\workspace\medicineDialecticFileAes\prescriptions.txt', 'r')

    try:
        pmfromText = pmfromf.readlines()
        prescriptionsText = prescriptionsf.readlines()
    finally:
        pmfromf.close()
        prescriptionsf.close()

    json_data = []

    for n in range(len(pmfromText)):

        pmfromTextLine = fg.fliggy(pmfromText[n].strip('\r\n'))
        prescriptionsTextLine = fg.fliggy(prescriptionsText[n].strip('\r\n'))

        prescriptionName = ""
        medicineReference = ""
        sourceFrom = ""

        pmfromTextLine = unicode(pmfromTextLine)
        splite_lis = re.split(u"。|，|：|、|--", pmfromTextLine)
        prescriptionName = splite_lis[0]

        prescriptionsTextLine = unicode(str(prescriptionsTextLine).strip())

        print prescriptionsTextLine

        if pmfromTextLine.find(u"--") is not -1:
            medicineReference = pmfromTextLine[pmfromTextLine.find(prescriptionName)+len(prescriptionName)+1:pmfromTextLine.find(u"--")]
            sourceFrom = pmfromTextLine[pmfromTextLine.find(u"--")+2:]
        json_data.append({"prescriptionName": prescriptionName, "medicineReference": medicineReference, "sourceFrom":
            sourceFrom, "prescriptionGroup": prescriptionsTextLine})

    return json.dumps(json_data)

# pmfromToJson()

