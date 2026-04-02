from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from decimal import Decimal
from django.db.models import Sum
from django.contrib import messages

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

from accounts.models import User
from .models import BankAccount, Transaction, FixedDeposit, Loan


# =========================
# CREATE ACCOUNT
# =========================
def create_account_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        account_type = request.POST.get("account_type")
        balance = request.POST.get("balance")

        email = request.POST.get("email")
        phone = request.POST.get("phone")
        aadhaar = request.POST.get("aadhaar").replace(" ", "")
        pan = request.POST.get("pan").replace(" ", "")
        address = request.POST.get("address")
        pincode = request.POST.get("pincode")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return redirect("create_account")

        if len(aadhaar) != 12 or not aadhaar.isdigit():
            messages.error(request, "Aadhaar must be 12 digits ❌")
            return redirect("create_account")

        if len(pan) != 10:
            messages.error(request, "PAN must be 10 characters ❌")
            return redirect("create_account")

        if len(pincode) != 6:
            messages.error(request, "Pincode must be 6 digits ❌")
            return redirect("create_account")

        user = User.objects.create_user(
            username=username,
            password=password,
            role="CUSTOMER"
        )

        account = BankAccount.objects.create(
            user=user,
            account_type=account_type,
            balance=balance,
            email=email,
            phone=phone,
            aadhaar=aadhaar,
            pan=pan,
            address=address,
            pincode=pincode
        )

        messages.success(request, "Account Created Successfully ✅")
        return render(request, "account_details.html", {"account": account})

    return render(request, "create_account.html")


# =========================
# WITHDRAW
# =========================
def withdraw_view(request):

    account = BankAccount.objects.filter(user=request.user).last()

    if request.method == 'POST':

        try:
            amount = Decimal(request.POST['amount'])
        except:
            messages.error(request, "Invalid amount ❌")
            return redirect("withdraw")

        if not account:
            messages.error(request, "Account not found ❌")
            return redirect("withdraw")

        if amount <= 0:
            messages.error(request, "Enter valid amount ❌")
            return redirect("withdraw")

        if account.balance < amount:
            messages.error(request, "Insufficient balance ❌")
            return redirect("withdraw")

        account.balance -= amount
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type="WITHDRAW",
            amount=amount
        )

        messages.success(request, "Withdrawal successful ✅")
        return redirect("withdraw")

    return render(request, 'withdraw.html', {'account': account})


# =========================
# TRANSFER
# =========================
def transfer_view(request):

    sender = BankAccount.objects.filter(user=request.user).last()

    if request.method == 'POST':

        acc_no = request.POST.get('account_number')
        amount = request.POST.get('amount')

        receiver = BankAccount.objects.filter(account_number=acc_no).first()

        if not receiver:
            messages.error(request, "Invalid account number ❌")
            return redirect("transfer")

        try:
            amount = Decimal(amount)
        except:
            messages.error(request, "Invalid amount ❌")
            return redirect("transfer")

        if amount <= 0:
            messages.error(request, "Enter valid amount ❌")
            return redirect("transfer")

        if not sender:
            messages.error(request, "Your account not found ❌")
            return redirect("transfer")

        if sender.balance < amount:
            messages.error(request, "Insufficient balance ❌")
            return redirect("transfer")

        sender.balance -= amount
        receiver.balance += amount

        sender.save()
        receiver.save()

        Transaction.objects.create(
            account=sender,
            transaction_type="TRANSFER",
            amount=amount
        )

        messages.success(request, "Transfer successful ✅")
        return redirect("transfer")

    return render(request, "transfer.html")


# =========================
# DEPOSIT
# =========================
def deposit_view(request):

    if request.method == "POST":

        acc_no = request.POST.get("account_number")
        amount = request.POST.get("amount")

        account = BankAccount.objects.filter(account_number=acc_no).first()

        if not account:
            messages.error(request, "Account not found ❌")
            return redirect("deposit")

        try:
            amount = Decimal(amount)
        except:
            messages.error(request, "Invalid amount ❌")
            return redirect("deposit")

        if amount <= 0:
            messages.error(request, "Amount must be greater than 0 ❌")
            return redirect("deposit")

        account.balance += amount
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type="DEPOSIT",
            amount=amount
        )

        messages.success(request, "Deposit successful ✅")
        return redirect("deposit")

    return render(request, "deposit.html")


# =========================
# HISTORY
# =========================
def history_view(request):

    account = BankAccount.objects.filter(user=request.user).last()
    txns = Transaction.objects.filter(account=account).order_by('-created_at')

    return render(request, 'history.html', {
        'transactions': txns,
        'account': account
    })


# =========================
# ⭐ PRO PDF STATEMENT
# =========================
def passbook_pdf_view(request):

    account = BankAccount.objects.filter(user=request.user).last()
    transactions = Transaction.objects.filter(account=account).order_by('-created_at')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bank_statement.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # 🏦 BANK HEADER
    elements.append(Paragraph("<b>BEBANK</b>", styles['Title']))
    elements.append(Spacer(1, 10))

    # 👤 CUSTOMER DETAILS
    elements.append(Paragraph(f"Name: {request.user.username}", styles['Normal']))
    elements.append(Paragraph(f"Account No: {account.account_number}", styles['Normal']))
    elements.append(Paragraph(f"Account Type: {account.account_type}", styles['Normal']))
    elements.append(Spacer(1, 10))

    # TABLE
    data = [["Date", "Type", "Credit (₹)", "Debit (₹)"]]

    for t in transactions:

        credit = ""
        debit = ""

        if t.transaction_type in ["DEPOSIT", "LOAN_CREDIT"]:
            credit = str(t.amount)
        else:
            debit = str(t.amount)

        data.append([
            t.created_at.strftime("%d-%m-%Y"),
            t.get_transaction_type_display(),
            credit,
            debit
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN',(2,1),(-1,-1),'RIGHT'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"<b>Available Balance: ₹{account.balance}</b>", styles['Heading2']))

    doc.build(elements)
    return response


# =========================
# FIXED DEPOSIT
# =========================
def fd_view(request):

    if request.method == 'POST':

        account = BankAccount.objects.filter(user=request.user).last()
        amount = request.POST.get("amount")

        try:
            amount = Decimal(amount)
        except:
            messages.error(request, "Invalid amount ❌")
            return redirect("fd")

        if amount <= 0:
            messages.error(request, "Amount must be greater than 0 ❌")
            return redirect("fd")

        if account.balance < amount:
            messages.error(request, "Insufficient balance ❌")
            return redirect("fd")

        account.balance -= amount
        account.save()

        FixedDeposit.objects.create(
            account=account,
            amount=amount,
            duration_months=int(request.POST['months'])
        )

        messages.success(request, "FD Booked Successfully 🎉")
        return redirect("fd")

    return render(request, 'fd.html')


# =========================
# LOAN APPLY
# =========================
def loan_view(request):

    if request.method == 'POST':

        account = BankAccount.objects.filter(user=request.user).last()
        amount = request.POST.get("amount")
        months = request.POST.get("months")

        try:
            amount = Decimal(amount)
        except:
            messages.error(request, "Invalid amount ❌")
            return redirect("loan")

        if amount <= 0:
            messages.error(request, "Amount must be greater than 0 ❌")
            return redirect("loan")

        if int(months) <= 0:
            messages.error(request, "Invalid duration ❌")
            return redirect("loan")

        Loan.objects.create(
            account=account,
            amount=amount,
            duration_months=int(months)
        )

        messages.success(request, "Loan Applied Successfully 🎉")
        return redirect("loan")

    return render(request, 'loan.html')


# =========================
# APPROVE LOAN
# =========================
def approve_loan(request, loan_id):

    loan = get_object_or_404(Loan, id=loan_id)

    if loan.status == "PENDING":

        account = loan.account
        account.balance += loan.amount
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type="LOAN_CREDIT",  # ✅ FIXED
            amount=loan.amount
        )

        loan.status = "APPROVED"
        loan.save()

    return redirect('/admin-dashboard/')


# =========================
# REJECT LOAN
# =========================
def reject_loan(request, loan_id):

    loan = get_object_or_404(Loan, id=loan_id)
    loan.status = "REJECTED"
    loan.save()

    return redirect('/admin-dashboard/')


# =========================
# ANALYTICS
# =========================
def analytics_view(request):

    total_accounts = BankAccount.objects.count()
    total_balance = BankAccount.objects.aggregate(Sum('balance'))['balance__sum'] or 0
    total_loans = Loan.objects.count()

    return render(request, "analytics.html", {
        "accounts": total_accounts,
        "balance": float(total_balance),
        "loans": total_loans
    })