# _*_ encoding:utf-8 _*_
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse
import simplejson, time, json
from django.views.decorators.csrf import csrf_exempt

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
        content = unicode(content)
        # content = unicode.decode(content, 'utf-8')
        lis = rank4Medicine(content, '')

        json_data = []

        for x in lis:
            json_data.append({"prescriptionName": x[0], "sourceFrom": x[1], "medicineReference": x[2],
                              "prescriptionGroup": x[3], "weight": x[4]})

        result = json.dumps(lis)
        return HttpResponse('{"status":"success","res":' + result + '}', content_type='application/json')


class MedicineReasoning(View):
    def get(self, request):
        return render(request, "medicine-reasoning.html")


class PrescriptionMatch(View):
    def post(self, request):
        print "PrescriptionMatch........"
        free_text = request.POST.get('free_text')
        if not isinstance(free_text, unicode):
            free_text = unicode(free_text)
        lis = getListout(free_text)
        return HttpResponse('{"status":"success", "lis":'+simplejson.dumps(lis)+'}', content_type='application/json')


class ChoiceLabel(View):
    def post(self, request):
        print 'ChoiceLabel....'
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
                print free_text
                lis = getListout(free_text.replace(u',', u'，'))
        return HttpResponse('{"status":"success", "lis":' + simplejson.dumps(lis) + '}', content_type='application/json')


class PrescriptionUnion(View):
    def get(self, request):
        cur_time = time.time()
        return render(request, "prescription-union.html",
                      {"cur_time": cur_time})


class ExternalRequest(View):
    def post(self, request):
        print "ExternalRequest..."
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


@csrf_exempt
def RestPrescription(request):
    if request.method == "POST":
        content = unicode(json.loads(request.body)['content'])
        lis = rank4Medicine(content, '')

        json_data = []

        for x in lis:
            json_data.append({"prescriptionName": x[0], "sourceFrom": x[1], "medicineReference": x[2],
                              "prescriptionGroup": x[3], "weight": x[4]})

        result = json.dumps(json_data)
        return HttpResponse('{"status":"success","res":' + result + '}', content_type='application/json')


@csrf_exempt
def RestExternal(request):
    if request.method == "POST":
        content = unicode(json.loads(request.body)['content'])
        params = {"patientSay": content}
        response = requests.post(DAJIAZHONGYI_URL, json=params)
        data = response.content
        data = unicode(data).encode("utf-8")
        return HttpResponse('{"status":"success","res":' + data + '}')


@csrf_exempt
def RestMedicineGroup(request):
    if request.method == "POST":
        content = unicode(json.loads(request.body)['content'])
        lis = rank4Medicine(content, '')

        json_data = []

        for x in lis:
            json_data.append({"prescriptionName": x[0], "sourceFrom": x[1], "medicineReference": x[2],
                              "prescriptionGroup": x[3], "weight": x[4]})

        return HttpResponse('{"status":"success","res":'+json.dumps(json_data)+'}', content_type='application/json')
