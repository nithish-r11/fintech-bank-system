from django.shortcuts import render
from .models import BankAccount
from decimal import Decimal

def withdraw_view(request):

    message = ""

    if request.method == 'POST':

        amount = Decimal(request.POST['amount'])

        try:
            account = BankAccount.objects.get(user=request.user)

            if account.balance >= amount:
                account.balance = account.balance - amount
                account.save()
                message = "Withdrawal Successful"
            else:
                message = "Insufficient Balance"

        except BankAccount.DoesNotExist:
            message = "Bank account not found"

    return render(request, 'withdraw.html', {'message': message})