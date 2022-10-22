import uuid

from django.db import models


class Paper(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    content = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)
    notes = models.TextField()


class School(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=1024)

    def info(self):
        content = {
            'id':self.uid,
            'school': self.name
        }
        return content


class Grade(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=1024)
    school = models.ForeignKey(School)

    def info(self):
        content = {
            'id':self.uid,
            'grade': self.name,
            'school': self.school.name,
            'school_id':self.school.uid
        }
        return content


class Class(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=1024)
    grade = models.ForeignKey(Grade)

    def get_school(self) -> School:
        return self.grade.school

    def info(self):
        content = {
            'id':self.uid
            'class': self.name,
            'grade': self.grade.name,
            'grade_id':self.grade.uid,
            'school': self.get_school().name,
            'school_id':self.get_school().id,
        }
        return content


class User(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=1024)
    stuClass = models.ForeignKey(Class)

    def get_grade(self) -> Grade:
        return self.stuClass.grade

    def get_school(self) -> School:
        return self.stuClass.get_school()


class Exam(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    paper = models.ForeignKey(Paper)


class Enrollment(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    exam = models.ForeignKey(Exam)
    user = models.ForeignKey(User)
    result = models.IntegerField()
    submit_time = models.DateTimeField()


def newUser(name: str, school: str, grade: str, stu_class: str):
    school: School = School.objects.filter(name=school).first()
    grade: Grade = Grade.objects.filter(name=grade, school=school).first()
    stu_class: Class = Class.objects.filter(name=stu_class, grade=grade)
    user: User = User(name, stu_class)
    return user
