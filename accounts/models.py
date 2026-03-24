from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('EMPLOYEE', 'Employee'),
        ('ADMIN', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.username