# _*_ encoding:utf-8 _*_
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse

import simplejson, time

import requests

from findSymptomVec import getListout
from medicineDialectic import rank4Medicine

from CandyOnline.settings import DAJIAZHONGYI_URL
# Create your views here.


class SavePrescription(View):
    def get(self, request):
        return render(request, "prescription.html")


class ReceivePrescription(View):
    def post(self, request):
        # time.sleep(10)
        content = request.POST.get("content")
        content = unicode.decode(content, 'utf-8')
        lis = rank4Medicine(content, '')
        # print lis

        result = simplejson.dumps(lis)
        return HttpResponse(result, content_type='application/json')


class MedicineReasoning(View):
    def get(self, request):
        return render(request, "medicine-reasoning.html")


class PrescriptionMatch(View):
    def post(self, request):
        free_text = request.POST.get('free_text')
        lis = []
        if free_text is not None:
            if not isinstance(free_text, unicode):
                free_text = unicode(free_text)
            lis = getListout(free_text)
        # lis = read4Vec(free_text)
        return HttpResponse('{"status":"success", "lis":'+simplejson.dumps(lis)+'}', content_type='application/json')


class ChoiceLabel(View):
    def post(self, request):
        free_text = request.POST.get('free_text')
        choice_labels = request.POST.get('choice_labels')
        unchoice_labels = request.POST.get('unchoice_labels')
        if free_text is not None and choice_labels is not None and unchoice_labels is not None:
            if free_text is not "" and choice_labels is not "" and unchoice_labels is not "":
                if not isinstance(free_text, unicode):
                    free_text = unicode(free_text)
                if not isinstance(choice_labels, unicode):
                    choice_labels = unicode(choice_labels)
                if not isinstance(unchoice_labels, unicode):
                    unchoice_labels = unicode(unchoice_labels)
                free_text = u"、"+choice_labels+u","+free_text
                free_text = unchoice_labels+free_text
                # print free_text
                lis = getListout(free_text.replace(u',', u'，'))
        return HttpResponse('{"status":"success", "lis":' + simplejson.dumps(lis) + '}', content_type='application/json')


class PrescriptionUnion(View):
    def get(self, request):
        cur_time = time.time()
        return render(request, "prescription-union.html",
                      {"cur_time": cur_time})


class ExternalRequest(View):
    def post(self, request):
        content = request.POST.get('content')
        params = {"patientSay": content}
        response = requests.post(DAJIAZHONGYI_URL, json=params)
        data = response.content
        return HttpResponse('{"status":"success","res":'+data+'}')


class MasterConsultation(View):
    def get(self, request):
        cur_time = time.time()
        return render(request, "master-consultation.html",
                      {"cur_time": cur_time})


class PrescriptionDetail(View):
    def get(self, request):
        return render(request, "prescription-detail.html")

