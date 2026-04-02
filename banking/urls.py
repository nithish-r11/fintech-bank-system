from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # ACCOUNT
    # =========================
    path('create-account/', views.create_account_view, name="create_account"),

    # =========================
    # TRANSACTIONS
    # =========================
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name="withdraw"),
    path('transfer/', views.transfer_view, name="transfer"),

    # =========================
    # HISTORY + PDF
    # =========================
    path('history/', views.history_view, name="history"),
    path('history/pdf/', views.passbook_pdf_view, name="history_pdf"),

    # ✅ OPTIONAL (no more 404)
    path('passbook/', views.passbook_pdf_view, name="passbook"),

    # =========================
    # BANK SERVICES
    # =========================
    path('fd/', views.fd_view, name="fd"),
    path('loan/', views.loan_view, name="loan"),

    # =========================
    # ANALYTICS
    # =========================
    path('analytics/', views.analytics_view, name="analytics"),
]