from django.db import models
from .user_model import UserModel

class CustomerModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)