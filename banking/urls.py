from django.urls import path
from . import views

urlpatterns = [

    path('create-account/', views.create_account_view, name="create_account"),

    path('withdraw/', views.withdraw_view, name="withdraw"),
    path('transfer/', views.transfer_view, name="transfer"),

    path('history/', views.history_view, name="history"),
    path('history/pdf/', views.passbook_pdf_view, name="history_pdf"),

    path('deposit/', views.deposit_view, name='deposit'),

    path('fd/', views.fd_view, name="fd"),
    path('loan/', views.loan_view, name="loan"),

    # ✅ FIXED
    path('analytics/', views.analytics_view, name="analytics"),
]