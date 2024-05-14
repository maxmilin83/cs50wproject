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
    balance = models.DecimalField(decimal_places=2,max_digits=15,default=10000)

    def __str__(self):
        return self.username