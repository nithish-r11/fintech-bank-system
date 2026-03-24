from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User


def role_select(request):
    return render(request, 'role_select.html')


def login_view(request, role):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.account_locked:
                return render(request, 'login.html', {'role': role, 'error': 'Account Locked'})

            if user.role.lower() == role:
                login(request, user)

                if role == 'customer':
                    return redirect('/customer/dashboard/')
                elif role == 'employee':
                    return redirect('/employee/dashboard/')
                elif role == 'admin':
                    return redirect('/admin-dashboard/')

            else:
                return render(request, 'login.html', {'role': role, 'error': 'Role mismatch'})

        else:
            try:
                u = User.objects.get(username=username)
                u.failed_login_attempts += 1
                if u.failed_login_attempts >= 3:
                    u.account_locked = True
                u.save()
            except:
                pass

            return render(request, 'login.html', {'role': role, 'error': 'Invalid credentials'})

    return render(request, 'login.html', {'role': role})


def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')


def employee_dashboard(request):
    return render(request, 'employee_dashboard.html')


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('/')