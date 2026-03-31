from django.contrib import admin
from django.urls import path, include
from banking.views import approve_loan, reject_loan

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),
    path('bank/', include('banking.urls')),

    path('approve-loan/<int:loan_id>/', approve_loan),
    path('reject-loan/<int:loan_id>/', reject_loan),
]