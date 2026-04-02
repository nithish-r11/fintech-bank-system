from django.db import models
from accounts.models import User
from decimal import Decimal
import random


class BankAccount(models.Model):

    ACCOUNT_TYPE = (
        ('SAVINGS', 'Savings'),
        ('CURRENT', 'Current'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    account_number = models.CharField(max_length=20, unique=True, blank=True)

    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)

    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # ⭐ NEW FIELDS
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    aadhaar = models.CharField(max_length=12, null=True, blank=True)
    pan = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        # ⭐ AUTO ACCOUNT NUMBER
        if not self.account_number:
            last = BankAccount.objects.order_by('-id').first()
            if last and last.account_number.isdigit():
                self.account_number = str(int(last.account_number) + 1)
            else:
                self.account_number = "10001"

        super().save(*args, **kwargs)

class Transaction(models.Model):

    TRANSACTION_TYPE = (
        ('WITHDRAW', 'Withdraw'),
        ('TRANSFER', 'Transfer'),
    )

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.account_number} - {self.transaction_type}"


class FixedDeposit(models.Model):

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('6.50'))
    duration_months = models.IntegerField()
    maturity_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        rate = Decimal(self.interest_rate)
        months = Decimal(self.duration_months)

        interest = (self.amount * rate * months) / Decimal('1200')
        self.maturity_amount = self.amount + interest

        super().save(*args, **kwargs)

    def __str__(self):
        return f"FD - {self.account.account_number}"


class Loan(models.Model):

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    duration_months = models.IntegerField()

    status = models.CharField(max_length=20, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.account_number} - {self.amount}"