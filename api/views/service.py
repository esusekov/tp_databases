__author__ = 'egor'

import json

from django.http import HttpResponse


def get_related_params(request_data):
    try:
        related_params = request_data["related"]
    except KeyError:
        related_params = []
    return related_params


def get_optional_params(request_data, possible_values):
    optional_params = {}
    for value in possible_values:
        try:
            optional_params[value] = request_data[value]
        except KeyError:
            continue
    return optional_params


def get_getrequest_params(request_data):
    data = {}
    for el in request_data.GET:
        data[el] = request_data.GET.get(el)
    return data


def positive_response(response_object):
    response_data = {"code": 0, "response": response_object}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def error_response(message):
    response_data = {"code": 1, "response": message}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def check_required_params(data, required):
    for el in required:
        if el not in data:
            raise Exception("req el " + el + " didnt requested")
        if data[el] is not None:
            try:
                data[el] = data[el].encode('utf-8')
            except Exception:
                continue

    return
