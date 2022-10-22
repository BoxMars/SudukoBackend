from data import models
from django.http import JsonResponse


def generate_response(data, code):
    code_ref = {
        0: ['General Error', 404],
        1: ['Success', 200],
        10001: ["School name is not listed", 404],
        10002: ['Grade name is not listed', 404],
    }
    res = {
        'code': code,
        'message': code_ref[code][0],
        data: data
    }
    return JsonResponse(res, status=code_ref[code][1])


def get_school_list(request):
    data = []
    school_list = models.School.objects.all()
    for school in school_list:
        data.append(school.info())
    return generate_response(data, 1)


def get_grade_list(request):
    school = request.GET.get('school')
    school = models.School.objects.filter(name=school)
    if len(school) == 0:
        return generate_response({}, 10001)
    school = school.first()
    grade_list = models.Grade.objects.filter(school=school)
    data = []
    for grade in grade_list:
        data.append(grade.info())
    return generate_response(data, 1)


def get_class_list(request):
    school = request.GET.get('school')
    grade = request.GET.get('grade')
    school = models.School.objects.filter(name=school)
    if len(school) == 0:
        return generate_response({}, 10001)
    school = school.first()
    grade = models.Grade.objects.filter(name=grade, school=school)
    if len(grade) == 0:
        return generate_response({}, 10002)
    grade = grade.first()
    stu_class_list = models.Class.objects.filter(grade=grade)
    data = []
    for stu_class in stu_class_list:
        data.append(stu_class.info())
    return generate_response(data, 1)
