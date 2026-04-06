from django.urls import path
from . import views

urlpatterns = [

    # ✅ SINGLE LOGIN PAGE
    path('', views.login_view, name="login"),

    # DASHBOARDS
    path('customer/dashboard/', views.customer_dashboard, name="customer_dashboard"),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # AUTH
    path('logout/', views.logout_view, name='logout'),

    # ADMIN CONTROLS
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('login/', views.login_view, name='login')

]