from django.shortcuts import render

def role_select(request):
    return render(request, 'role_select.html')