# _*_ encoding:utf-8 _*_mi
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class ScrapMedicine(models.Model):
    diseaseName = models.CharField(max_length=500, verbose_name=u"病名")
    patientContent = models.CharField(max_length=500, verbose_name=u"患者")
    contentVec = models.CharField(max_length=500, null=True)
    prescriptionName = models.CharField(max_length=500, verbose_name=u"开方名")
    prescriptions = models.CharField(max_length=500, verbose_name=u"开方")
    prescriptionsReasons = models.CharField(max_length=500, null=True, verbose_name=u"开方原因")
    sourceFrom = models.CharField(max_length=500, verbose_name=u"来源", default=u"胡希恕伤寒方证辩证")


class PrescriptionScrapmedicine(models.Model):
    diseaseName = models.CharField(max_length=500, verbose_name=u"病名")
    patientContent = models.CharField(max_length=500, verbose_name=u"患者")
    contentVec = models.CharField(max_length=500, null=True)
    prescriptionName = models.CharField(max_length=500, verbose_name=u"开方名")
    prescriptions = models.CharField(max_length=500, verbose_name=u"开方")
    prescriptionsReasons = models.CharField(max_length=500, null=True, verbose_name=u"开方原因")
    sourceFrom = models.CharField(max_length=500, verbose_name=u"来源", default=u"胡希恕伤寒方证辩证")
