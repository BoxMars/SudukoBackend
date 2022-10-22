from django.db import models


class Paper(models.Model):
    content = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)
    notes = models.TextField()


class School(models.Model):
    name = models.CharField(max_length=1024)

    def info(self):
        content = {
            'school': self.name
        }
        return content


class Grade(models.Model):
    name = models.CharField(max_length=1024)
    school = models.ForeignKey(School)

    def info(self):
        content = {
            'grade': self.name,
            'school': self.school.name
        }
        return content


class Class(models.Model):
    name = models.CharField(max_length=1024)
    grade = models.ForeignKey(Grade)

    def get_school(self) -> School:
        return self.grade.school

    def info(self):
        content = {
            'class': self.name,
            'grade': self.grade.name,
            'school': self.get_school().name
        }
        return content


class User(models.Model):
    name = models.CharField(max_length=1024)
    stuClass = models.ForeignKey(Class)

    def get_grade(self) -> Grade:
        return self.stuClass.grade

    def get_school(self) -> School:
        return self.stuClass.get_school()


class Exam(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    paper = models.ForeignKey(Paper)


class Enrollment(models.Model):
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
