# _*_ encoding:utf-8 _*_
import requests


def use_params_requests():
    URL_IP = "http://static.dev.studio.dajiazhongyi.com:8081/search/cases"
    params = {"patientSay": "发烧，头痛，有汗，怕冷，经期，脉弦细，舌苔白腻"}
    response = requests.post(URL_IP, json=params)
#     print 'response Headers:'
#     print response.headers
#     print 'response Body:'
    print response.content
#
# use_params_requests()
