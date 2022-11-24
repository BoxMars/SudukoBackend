import uuid

from django.db import models


class Paper(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    content = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)
    notes = models.TextField(default="")

    def info(self):
        res = {
            'uid': self.uid,
            'content': self.content,
        }
        return res


class User(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=1024)
    phone = models.CharField(max_length=1024)

    def info(self):
        res = {
            'uid': self.uid,
            'name': self.name,
            'phone': self.phone
        }
        return res


class Exam(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.IntegerField(default=0)
    paper1 = models.ForeignKey(Paper, on_delete=models.DO_NOTHING, related_name='paper1')
    paper2 = models.ForeignKey(Paper, on_delete=models.DO_NOTHING, related_name='paper2')

    def info(self):
        res={
            'uid':self.uid,
            'start':self.start_time,
            'end':self.end_time,
            'paper1':self.paper1.info(),
            'paper2':self.paper2.info()
        }
        return res

class Enrollment(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    exam = models.ForeignKey(Exam, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    paper1_answer = models.CharField(max_length=1024)
    paper2_answer = models.CharField(max_length=1024)
    result = models.IntegerField(default=-1)
    submit_time = models.DateTimeField(null=True,blank=True)

    def get_result(self):
        return 1