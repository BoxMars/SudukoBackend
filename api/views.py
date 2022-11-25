import time

from data import models
from django.http import JsonResponse
import jwt
from django.utils.timezone import now


def generate_response(data, code):
    code_ref = {
        0: ['General Error', 500],
        1: ['Success', 200],
        10001: ['User is not listed or not matched with phone number', 404],
        10002: ['Login again', 500],
        10003: ["This user don't enroll any exam", 404],
    }
    res = {
        'code': code,
        'message': code_ref[code][0],
        'data': data
    }
    return JsonResponse(res, status=code_ref[code][1])


def sign_in(request):
    name = request.POST.get('name',"")
    phone = request.POST.get('phone',"")

    user_list = models.User.objects.filter(name=name, phone=phone)
    if len(user_list) == 0:
        return generate_response({}, 10001)

    jet_content = {
        'name': name,
        'phone': phone,
        'id': user_list.first().phone,
        "exp": time.time() + 7 * 24 * 60 * 60
    }
    key = '1234'

    jwt_result = jwt.encode(jet_content, key, algorithm='HS256')

    response = generate_response({}, 1)
    response.set_cookie('account', jwt_result)
    return response

def get_user(request):
    print(request.COOKIES)
    jwt_content = request.COOKIES['account']
    key = '1234'
    try:
        info = jwt.decode(jwt_content, key, algorithms=['HS256'])
    except:
        return 0, generate_response({}, 10002)
    user = models.User.objects.filter(phone=info['phone'])

    if len(user) == 0:
        return 0, generate_response({}, 10001)

    user = user.first()
    return 1, user

def get_paper(request):

    code,user=get_user(request)

    if code==0:
        return user

    enrollment=models.Enrollment.objects.filter(user=user)

    if len(enrollment)==0:
        return generate_response({}, 10003)

    res=enrollment.first().exam.info()
    return generate_response(res,1)

def submit_paper(request):
    """
    POST
    :param request: {
                        paper1: ans in one line,
                        paper2: ans in one line,
                    }
    :return:
    """
    code, user=get_user(request)

    if code==0:
        return user

    enrollment = models.Enrollment.objects.filter(user=user)

    if len(enrollment) == 0:
        return generate_response({}, 10003)

    enrollment=enrollment.first()

    paper1=request.POST.get('paper1',"")
    paper2=request.POST.get('paper2',"")

    enrollment.paper1_answer=paper1
    enrollment.paper2_answer=paper2

    enrollment.submit_time=now()

    enrollment.result=enrollment.get_result()

    enrollment.save()

    return generate_response({},1)

def test(re):
    user = models.User.objects.filter(name='a').first()
    exam=models.Exam.objects.filter(uid__exact='66afc201755245d0881f8b448e991694').first()
    eroolment=models.Enrollment(
        exam=exam,
        user=user,
    )
    eroolment.save()
    return generate_response({},1)