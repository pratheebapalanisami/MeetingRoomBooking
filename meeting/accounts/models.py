from django.contrib.auth.models import AbstractUser
from django.db import models

from meeting import settings

class CustomUser(AbstractUser):
   pass

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=50)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)





