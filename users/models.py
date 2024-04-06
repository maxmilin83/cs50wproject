from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):

    STATUS = {
        ('regular','regular'),
        ('moderator','moderator')
    }

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100,choices=STATUS, default='regular')
    balance = models.IntegerField(default=5000)

    def __str__(self):
        return self.username