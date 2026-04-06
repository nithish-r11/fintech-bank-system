from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home_redirect(request):
    return redirect('/login/')   # ✅ FIXED


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_redirect),   # root redirect

    path('', include('accounts.urls')),
    path('bank/', include('banking.urls')),
]