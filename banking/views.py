from django.shortcuts import render
from .models import BankAccount, Transaction
from decimal import Decimal
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from accounts.models import User
from .models import FixedDeposit
from .models import Loan


def create_account_view(request):

    message = ""

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        acc_type = request.POST['account_type']
        balance = Decimal(request.POST['balance'])

        user = User.objects.create_user(
            username=username,
            password=password,
            role='CUSTOMER'
        )

        BankAccount.objects.create(
            user=user,
            account_type=acc_type,
            balance=balance
        )

        message = "Customer Account Created Successfully"

    return render(request, 'create_account.html', {'message': message})


# ------- existing functions below --------

def withdraw_view(request):
    message = ""
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        try:
            account = BankAccount.objects.get(user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, transaction_type='WITHDRAW', amount=amount)
                message = "Withdrawal Successful"
            else:
                message = "Insufficient Balance"
        except:
            message = "Bank account not found"
    return render(request, 'withdraw.html', {'message': message})


def transfer_view(request):
    message = ""
    if request.method == 'POST':
        acc_no = request.POST['account_number']
        amount = Decimal(request.POST['amount'])
        try:
            sender = BankAccount.objects.get(user=request.user)
            receiver = BankAccount.objects.get(account_number=acc_no)
            if sender.balance >= amount:
                sender.balance -= amount
                receiver.balance += amount
                sender.save()
                receiver.save()
                Transaction.objects.create(account=sender, transaction_type='TRANSFER', amount=amount)
                message = "Transfer Successful"
            else:
                message = "Insufficient Balance"
        except:
            message = "Invalid Receiver Account"
    return render(request, 'transfer.html', {'message': message})


def history_view(request):
    try:
        account = BankAccount.objects.get(user=request.user)
        transactions = Transaction.objects.filter(account=account).order_by('-created_at')
    except:
        transactions = []
    return render(request, 'history.html', {'transactions': transactions})


def passbook_pdf(request):
    account = BankAccount.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="passbook.pdf"'

    p = canvas.Canvas(response)
    y = 800
    p.drawString(200, 820, "Fintech Bank Passbook")

    for t in transactions:
        text = f"{t.transaction_type}   {t.amount}   {t.created_at}"
        p.drawString(50, y, text)
        y -= 20

    p.showPage()
    p.save()

    return response


def deposit_view(request):
    message = ""
    if request.method == 'POST':
        acc_no = request.POST['account_number']
        amount = Decimal(request.POST['amount'])
        try:
            account = BankAccount.objects.get(account_number=acc_no)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, transaction_type='TRANSFER', amount=amount)
            message = "Deposit Successful"
        except:
            message = "Invalid Account Number"
    return render(request, 'deposit.html', {'message': message})
from decimal import Decimal
from .models import FixedDeposit

def fd_view(request):

    message = ""

    if request.method == 'POST':

        amount = Decimal(request.POST['amount'])
        months = int(request.POST['months'])

        account = BankAccount.objects.filter(user=request.user).first()

        if not account:
            message = "No savings account found for this user"
        else:

            if account.balance >= amount:

                account.balance -= amount
                account.save()

                FixedDeposit.objects.create(
                    account=account,
                    amount=amount,
                    duration_months=months
                )

                message = "FD Booked Successfully"

            else:
                message = "Insufficient Balance"

    return render(request, 'fd.html', {'message': message})
from decimal import Decimal

def loan_view(request):

    message = ""

    if request.method == 'POST':

        amount = Decimal(request.POST['amount'])
        months = int(request.POST['months'])

        try:
            account = BankAccount.objects.get(user=request.user)

            Loan.objects.create(
                account=account,
                amount=amount,
                duration_months=months
            )

            message = "Loan Application Submitted Successfully"

        except:
            message = "Bank Account Not Found"

    return render(request, 'loan.html', {'message': message})