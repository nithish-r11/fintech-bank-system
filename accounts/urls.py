from django.urls import path
from . import views

urlpatterns = [

    path('', views.role_select),

    path('login/<str:role>/', views.login_view),

    path('customer/dashboard/', views.customer_dashboard),
    path('employee/dashboard/', views.employee_dashboard),
    path('admin-dashboard/', views.admin_dashboard),

    path('logout/', views.logout_view),

    # BLOCK / UNBLOCK
    path('block/<int:user_id>/', views.block_user),
    path('unblock/<int:user_id>/', views.unblock_user),

    # LOAN APPROVAL
    path('approve-loan/<int:loan_id>/', views.approve_loan),
    path('reject-loan/<int:loan_id>/', views.reject_loan),
]