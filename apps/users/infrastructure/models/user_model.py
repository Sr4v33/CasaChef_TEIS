from django.db import models

class UserModel(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)