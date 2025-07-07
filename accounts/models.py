from django.contrib.auth.models import AbstractUser
from django.db import models
# defines a custom user model that extends Django's AbstractUser 

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username