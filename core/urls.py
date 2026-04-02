from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views   # ✅ ADD THIS
from banking.views import approve_loan, reject_loan

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),
    path('bank/', include('banking.urls')),

    path('approve-loan/<int:loan_id>/', approve_loan),
    path('reject-loan/<int:loan_id>/', reject_loan),

    # ✅ ADD THIS LINE
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]