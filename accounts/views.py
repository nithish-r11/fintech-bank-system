from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db import models
from .models import User
from banking.models import BankAccount, Transaction, Loan


def role_select(request):
    return render(request, 'role_select.html')


def login_view(request, role):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.account_locked:
                return render(request, 'login.html', {
                    'role': role,
                    'error': 'Account Locked by Admin'
                })

            if user.role.lower() == role:
                login(request, user)

                if role == 'customer':
                    return redirect('/customer/dashboard/')
                elif role == 'employee':
                    return redirect('/employee/dashboard/')
                elif role == 'admin':
                    return redirect('/admin-dashboard/')

            else:
                return render(request, 'login.html', {
                    'role': role,
                    'error': 'Role mismatch'
                })

        else:
            return render(request, 'login.html', {
                'role': role,
                'error': 'Invalid credentials'
            })

    return render(request, 'login.html', {'role': role})


def customer_dashboard(request):

    try:
        account = BankAccount.objects.get(user=request.user)
        balance = account.balance
    except:
        balance = 0

    return render(request, 'customer_dashboard.html', {'balance': balance})


def employee_dashboard(request):
    return render(request, 'employee_dashboard.html')


def admin_dashboard(request):

    total_customers = User.objects.filter(role='CUSTOMER').count()
    total_employees = User.objects.filter(role='EMPLOYEE').count()
    total_balance = BankAccount.objects.all().aggregate(models.Sum('balance'))['balance__sum'] or 0
    total_transactions = Transaction.objects.count()

    customers_list = User.objects.filter(role='CUSTOMER')
    loans = Loan.objects.all()

    context = {
        'customers': total_customers,
        'employees': total_employees,
        'balance': total_balance,
        'transactions': total_transactions,
        'customers_list': customers_list,
        'loans': loans
    }

    return render(request, 'admin_dashboard.html', context)


def block_user(request, user_id):

    user = get_object_or_404(User, id=user_id)
    user.account_locked = True
    user.save()

    return redirect('/admin-dashboard/')


def unblock_user(request, user_id):

    user = get_object_or_404(User, id=user_id)
    user.account_locked = False
    user.save()

    return redirect('/admin-dashboard/')


def approve_loan(request, loan_id):

    loan = Loan.objects.get(id=loan_id)
    loan.status = "APPROVED"
    loan.save()

    return redirect('/admin-dashboard/')


def reject_loan(request, loan_id):

    loan = Loan.objects.get(id=loan_id)
    loan.status = "REJECTED"
    loan.save()

    return redirect('/admin-dashboard/')


def logout_view(request):
    logout(request)
    return redirect('/')