from django.db import models
from .user_model import UserModel

class CookModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)