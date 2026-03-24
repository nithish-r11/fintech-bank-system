from django.db import models
from accounts.models import User
import random

class BankAccount(models.Model):

    ACCOUNT_TYPE = (
        ('SAVINGS','Savings'),
        ('CURRENT','Current'),
        ('FD','Fixed Deposit'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=12, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = str(random.randint(100000000000,999999999999))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.account_number