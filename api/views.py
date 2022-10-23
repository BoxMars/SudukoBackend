from data import models
from django.http import JsonResponse


def generate_response(data, code):
    code_ref = {
        0: ['General Error', 404],
        1: ['Success', 200],
    }
    res = {
        'code': code,
        'message': code_ref[code][0],
        data: data
    }
    return JsonResponse(res, status=code_ref[code][1])


