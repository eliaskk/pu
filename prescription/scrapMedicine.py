# _*_ encoding:utf-8 _*_


# Create your tests here.


def prescriptionTreatment(fileName):
    f = open(fileName, 'r')
    # 病名
    diseaseNames = []
    # 开方名
    prescriptionNames = []
    # 患者
    patientContents = []
    # 开方
    prescriptions = []
    for line in f:
        content = unicode(line, 'utf-8')
        # print content
        if content.startswith(u'病名：'):
            diseaseName = content[3:]
            diseaseNames.append(diseaseName)
        elif content.startswith(u'开方'):
            str = content[3:]
            # 开方名
            prescriptionName = str[0:str.find(u"：")]
            # 开方
            prescription = str[str.find(u"：")+1:]
            prescriptionNames.append(prescriptionName)
            prescriptions.append(prescription)
        elif content.startswith(u'主诉：'):
            str = content[3:]
            patientContents.append(str)

    for x in range(len(diseaseNames)):
        pass
        # scrapMedicine = ScrapMedicine()
        # scrapMedicine.diseaseName = diseaseNames[x]
        # scrapMedicine.patientContent = patientContents[x]
        # scrapMedicine.prescriptionName = prescriptionNames[x]
        # scrapMedicine.prescriptions = prescriptions[x]
        # scrapMedicine.save()


