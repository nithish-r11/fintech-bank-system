from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect   # ⭐ ADD THIS

from banking.views import approve_loan, reject_loan


# ⭐ HOME REDIRECT FUNCTION
def home_redirect(request):
    return redirect('/login/CUSTOMER/')   # or '/login/' if you use single login


urlpatterns = [
    path('admin/', admin.site.urls),

    # ⭐ ROOT URL FIX
    path('', home_redirect),

    path('', include('accounts.urls')),
    path('bank/', include('banking.urls')),

    path('approve-loan/<int:loan_id>/', approve_loan),
    path('reject-loan/<int:loan_id>/', reject_loan),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]