from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('EMPLOYEE', 'Employee'),
        ('ADMIN', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    account_locked = models.BooleanField(default=False)

    # ⭐ login security fields
    failed_login_attempts = models.IntegerField(default=0)

    # ⭐ KYC + profile fields
    phone = models.CharField(max_length=15, blank=True, null=True)
    aadhaar = models.CharField(max_length=20, blank=True, null=True)
    pan = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    kyc_verified = models.BooleanField(default=False)