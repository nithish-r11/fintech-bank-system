from django.urls import path
from . import views

urlpatterns = [
    path('', views.role_select),

    path('login/<str:role>/', views.login_view),

    path('customer/dashboard/', views.customer_dashboard),
    path('employee/dashboard/', views.employee_dashboard),
    path('admin-dashboard/', views.admin_dashboard),

    path('logout/', views.logout_view),
]