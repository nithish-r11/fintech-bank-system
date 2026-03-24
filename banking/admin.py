from django.contrib import admin
from .models import BankAccount, Transaction, FixedDeposit

admin.site.register(BankAccount)
admin.site.register(Transaction)
admin.site.register(FixedDeposit)