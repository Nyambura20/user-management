from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username
# This code defines a custom user model that extends Django's AbstractUser.