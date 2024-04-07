from django.db import models
from django.conf import settings 
from datetime import datetime

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    action = models.CharField(blank=False,choices=(("buy","BUY"),("sell","SELL")),max_length=4)
    coin = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    amount = models.DecimalField(decimal_places=2,max_digits=10)
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.user.username} {self.action} {self.coin}"

