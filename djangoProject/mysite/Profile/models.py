from django.db import models
from django.http import HttpResponse

# Create your models here.

class PersonalProfile(models.Model):

    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    nick_name = models.CharField(max_length=20)
    age = models.CharField(max_length=25)


    def __str__(self):
        return self.f_name + ' ' + self.l_name


class Item(models.Model):

    profile = models.ForeignKey(PersonalProfile, on_delete=models.CASCADE)

    item_name = models.CharField(max_length=30)
    item_link = models.CharField(max_length=250)


