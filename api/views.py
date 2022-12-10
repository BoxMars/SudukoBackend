import time

from api.utils import generateFromStr
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
    name = request.POST['name']
    phone = request.POST['phone']

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

    paper1=request.POST['paper1']
    try:
        paper2=request.POST['paper2']
    except Exception:
        papre2=""

    enrollment.paper1_answer=paper1
    enrollment.paper2_answer=paper2

    enrollment.submit_time=now()

    enrollment.result=enrollment.get_result()

    enrollment.save()

    return generate_response({},1)

def newExam(r):
    paper=models.Paper(notes='福田1',content="8       4 2  3  6   51629    2 4 6   465 831   1 7 8    43572   3  8  5 2       6",answer="")
    paper.save()
    empty_paper=models.Paper.objects.filter(uid='92f98c71708245bbb6a00ec12f5a2c51').first()

    exam=models.Exam(
        start_time=now(),
        end_time=now(),
        status=1,
        paper1=paper,
        paper2=empty_paper,
    )
    exam.save()
    return generate_response({}, 1)
def newEnrollment(r):
    exam_uid="6ee16528f56347e0bae38c20d0e8bfae"
    exam=models.Exam.objects.filter(uid=exam_uid).first()
    l=generateFromStr('''汪子诺	15920034162
徐俪莹	13927456408
汪晓荣	15920034162
徐俪茗	18503007329
赵子铭	13423739279
汪子诺	15920034162
钟崇集	15002063010
钟育珩	15002063010
王楠	13714002030
赵余思欢	13560407477
于潇楠	18682408855
王昱祺	18682408855
潘其轩	15002066393
李望深	18589067266
陶俊宏	13760140223
洪子涵	13613095542
张伟	15013614715
蓝沁	13510172556
蓝萱	13510172556
罗莉	19926563121
丘宇骞	13631572958
岳一凡	15302790816
杨筱璐	13923489780
谢林跃	18926596122
谭芯可	18689201012
王菁睿	13691898693
冯博昱	13686806436''')
    for i in l:
        if len(models.User.objects.filter(phone=i[1]))!=0:
            t=models.User.objects.filter(phone=i[1]).first()
            t.name=i[0]
            t.save()
            enroll = models.Enrollment(
                user=t,
                exam=exam,
            )
            enroll.save()
            continue
        user = models.User(
            name=i[0],
            phone=i[1]
        )
        user.save()
        enroll = models.Enrollment(
            user=user,
            exam=exam,
        )
        enroll.save()
    return generate_response({}, 1)

def test(re):
    l=[
        # ['徐俪莹','13927456408'],
        # ['徐俪茗','18503007329'],
        # ['罗莉','19926563121'],
        # ['李望深','18589067266'],
        # ['赵子铭','13423739279'],
        # ['汪子诺','15920034162'],
        # ['汪晓荣','18617150996'],
        # ['钟崇集','15002063010'],
        # ['钟育珩','18188625136'],
        # ['王楠','13714002030'],
        # ['张怡然','15013614715']，
        # ['洪子涵','13613095542'],
        # ['于潇楠','18682408855'],
        # ['王昱祺','18682408877'],
        ['谢林跃','18926596122'],
        ['谭芯可','18689201012'],
        ['张伟','15013614715'],
    ]
    for i in l:
        user = models.User(
            name=i[0],
            phone=i[1]
        )
        user.save()
        exam=models.Exam.objects.filter(uid='66afc201755245d0881f8b448e991694').first()
        enroll=models.Enrollment(
            user=user,
            exam=exam,
        )
        enroll.save()
    return generate_response({},1)