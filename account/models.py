from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager


# Create your models here.


class User(AbstractUser):
    full_name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=11, unique=True)

    objects = UserManager()

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"

    class Meta:
        verbose_name_plural = 'users'


class Otp(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.CharField(max_length=4)
    created = models.DateTimeField(auto_now=True)
