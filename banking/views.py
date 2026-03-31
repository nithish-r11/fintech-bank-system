from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from decimal import Decimal
from reportlab.pdfgen import canvas

from accounts.models import User
from .models import BankAccount, Transaction, FixedDeposit, Loan


def create_account_view(request):

    if request.method == 'POST':

        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            role='CUSTOMER'
        )

        BankAccount.objects.create(
            user=user,
            account_type=request.POST['account_type'],
            balance=Decimal(request.POST['balance'])
        )

    return render(request, 'create_account.html')


def withdraw_view(request):

    if request.method == 'POST':

        account = BankAccount.objects.filter(user=request.user).last()
        amount = Decimal(request.POST['amount'])

        if account.balance >= amount:
            account.balance -= amount
            account.save()

            Transaction.objects.create(account=account, transaction_type='WITHDRAW', amount=amount)

    return render(request, 'withdraw.html')


def transfer_view(request):

    if request.method == 'POST':

        sender = BankAccount.objects.filter(user=request.user).last()
        receiver = BankAccount.objects.get(account_number=str(request.POST['account_number']))
        amount = Decimal(request.POST['amount'])

        if sender.balance >= amount:
            sender.balance -= amount
            receiver.balance += amount

            sender.save()
            receiver.save()

            Transaction.objects.create(account=sender, transaction_type='TRANSFER', amount=amount)

    return render(request, 'transfer.html')


def deposit_view(request):

    if request.method == 'POST':

        account = BankAccount.objects.get(account_number=str(request.POST['account_number']))
        amount = Decimal(request.POST['amount'])

        account.balance += amount
        account.save()

        Transaction.objects.create(account=account, transaction_type='TRANSFER', amount=amount)

    return render(request, 'deposit.html')


def history_view(request):

    account = BankAccount.objects.filter(user=request.user).last()
    txns = Transaction.objects.filter(account=account).order_by('-created_at')

    return render(request, 'history.html', {'transactions': txns})


def passbook_pdf_view(request):

    acc = BankAccount.objects.filter(user=request.user).last()
    txns = Transaction.objects.filter(account=acc)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="statement.pdf"'

    p = canvas.Canvas(response)
    y = 800

    for t in txns:
        p.drawString(50, y, f"{t.created_at.strftime('%d-%m-%Y')} {t.transaction_type} ₹{t.amount}")
        y -= 25

    p.save()
    return response


def fd_view(request):

    if request.method == 'POST':

        account = BankAccount.objects.filter(user=request.user).last()
        amount = Decimal(request.POST['amount'])

        if account.balance >= amount:
            account.balance -= amount
            account.save()

            FixedDeposit.objects.create(
                account=account,
                amount=amount,
                duration_months=int(request.POST['months'])
            )

    return render(request, 'fd.html')


def loan_view(request):

    if request.method == 'POST':

        account = BankAccount.objects.filter(user=request.user).last()

        Loan.objects.create(
            account=account,
            amount=Decimal(request.POST['amount']),
            duration_months=int(request.POST['months'])
        )

    return render(request, 'loan.html')


def approve_loan(request, loan_id):

    loan = get_object_or_404(Loan, id=loan_id)

    if loan.status == "PENDING":

        account = loan.account
        account.balance += loan.amount
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type="TRANSFER",
            amount=loan.amount
        )

        loan.status = "APPROVED"
        loan.save()

    return redirect('/admin-dashboard/')


def reject_loan(request, loan_id):

    loan = get_object_or_404(Loan, id=loan_id)
    loan.status = "REJECTED"
    loan.save()

    return redirect('/admin-dashboard/')