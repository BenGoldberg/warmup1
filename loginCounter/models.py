from django.db import models

class Users(models.Model):
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    count = models.IntegerField()
