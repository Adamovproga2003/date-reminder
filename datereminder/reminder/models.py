from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=200)
    birthDay = models.DateField("person's birthday")
    relationship = models.CharField(max_length=200)
