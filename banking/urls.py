from django.urls import path
from . import views

urlpatterns = [

    path('create-account/', views.create_account_view),

    path('withdraw/', views.withdraw_view),
    path('transfer/', views.transfer_view),

    path('history/', views.history_view),
    path('history/pdf/', views.passbook_pdf_view),

    path('deposit/', views.deposit_view),

    path('fd/', views.fd_view),
    path('loan/', views.loan_view),

]