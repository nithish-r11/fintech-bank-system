from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),   # root login

    path('login/', views.login_view, name='login'),

    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),

    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('logout/', views.logout_view, name='logout'),

    path('create-admin/', views.create_admin),
]