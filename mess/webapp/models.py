from django.db import models

from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class Record(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)

    firstName = models.CharField(max_length=100)

    lastName = models.CharField(max_length=100)

    email = models.CharField(max_length=255)

    phone = models.CharField(max_length=20)

    address = models.CharField(max_length=300)

    city = models.CharField(max_length=255)

    province = models.CharField(max_length=255)

    country = models.CharField(max_length=125)


    def __str__(self):
        return self.firstName + " " + self.lastName

















