import time

from data import models
from django.http import JsonResponse
import jwt


def generate_response(data, code):
    code_ref = {
        0: ['General Error', 500],
        1: ['Success', 200],
        10001: ['User is not listed', 404]
    }
    res = {
        'code': code,
        'message': code_ref[code][0],
        data: data
    }
    return JsonResponse(res, status=code_ref[code][1])


def sign_in(request):
    name = request.POST['name']
    phone = request.POST['phone']

    user_list = models.User.objects.filter(name=name, phone=phone)
    if len(user_list) == 0:
        return generate_response({}, 10001)

    jet_content = {
        'name': name,
        'phone': phone,
        "exp": time.time() + 7 * 24 * 60 * 60
    }
    key = '1234'

    jwt_result = jwt.encode(jet_content, key, algorithm='HS256')

    response = generate_response({}, 1)
    response.set_cookie('account', jwt_result)
    return response

def get_paper(request):
    pass
