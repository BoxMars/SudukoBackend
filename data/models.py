import uuid

from django.db import models


class Paper(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    content = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)
    notes = models.TextField()


class User(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=1024)
    phone = models.CharField(max_length=1024)


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
