from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse   # ✅ IMPORTANT ADD

from .models import User
from banking.models import BankAccount, Transaction, Loan


# =========================
# ✅ SINGLE LOGIN
# =========================
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # 🔴 BLOCK CHECK
            if getattr(user, "account_locked", False):
                messages.error(request, "Account is blocked ❌")
                return redirect("login")

            # 🔴 ROLE CHECK
            if user.role != role:
                messages.error(request, "Invalid role selected ❌")
                return redirect("login")

            login(request, user)

            # 🔀 REDIRECT BASED ON ROLE
            if role == "CUSTOMER":
                return redirect("/customer/dashboard/")
            elif role == "EMPLOYEE":
                return redirect("/employee/dashboard/")
            elif role == "ADMIN":
                return redirect("/admin-dashboard/")

        else:
            messages.error(request, "Invalid username or password ❌")

    return render(request, "login.html")


# =========================
# CUSTOMER DASHBOARD
# =========================
def customer_dashboard(request):

    account = BankAccount.objects.filter(user=request.user).last()

    return render(request, "customer_dashboard.html", {
        "account": account
    })


# =========================
# EMPLOYEE DASHBOARD
# =========================
def employee_dashboard(request):

    total_accounts = BankAccount.objects.count()
    total_balance = BankAccount.objects.aggregate(Sum('balance'))['balance__sum'] or 0
    total_loans = Loan.objects.count()

    account = None

    if request.method == "POST":
        acc_no = request.POST.get("account_number")
        account = BankAccount.objects.filter(account_number=acc_no).first()

        if not account:
            messages.error(request, "Account not found ❌")

    return render(request, "employee_dashboard.html", {
        "accounts": total_accounts,
        "balance": total_balance,
        "loans": total_loans,
        "account": account
    })


# =========================
# ADMIN DASHBOARD
# =========================
def admin_dashboard(request):

    total_customers = User.objects.filter(role='CUSTOMER').count()
    total_employees = User.objects.filter(role='EMPLOYEE').count()
    total_balance = BankAccount.objects.aggregate(Sum('balance'))['balance__sum'] or 0
    total_transactions = Transaction.objects.count()

    loans = Loan.objects.all()

    return render(request, 'admin_dashboard.html', {
        'customers': total_customers,
        'employees': total_employees,
        'balance': total_balance,
        'transactions': total_transactions,
        'loans': loans
    })


# =========================
# BLOCK USER
# =========================
def block_user(request, user_id):

    user = get_object_or_404(User, id=user_id)
    user.account_locked = True
    user.save()

    messages.success(request, "User blocked 🚫")

    return redirect('/admin-dashboard/')


# =========================
# UNBLOCK USER
# =========================
def unblock_user(request, user_id):

    user = get_object_or_404(User, id=user_id)
    user.account_locked = False
    user.save()

    messages.success(request, "User unblocked ✅")

    return redirect('/admin-dashboard/')


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect('/login/')


# =========================
# 🔥 CREATE ADMIN (FOR RENDER)
# =========================
def create_admin(request):

    if not User.objects.filter(username="BEBANK").exists():
        User.objects.create_user(
            username="BEBANK",
            password="2006",
            role="ADMIN"
        )
        return HttpResponse("Admin created ✅")

    return HttpResponse("Admin already exists 👍")

def create_employee(request):

    if not User.objects.filter(username="employee1").exists():
        User.objects.create_user(
            username="NITHISH KUMAR",
            password="black2006",
            role="EMPLOYEE"
        )
        return HttpResponse("Employee created ✅")

    return HttpResponse("Employee already exists 👍")