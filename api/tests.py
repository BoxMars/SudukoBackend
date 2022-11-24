from data import models

user=models.User(
  name='a',
  phone='123456'
)
user.save()