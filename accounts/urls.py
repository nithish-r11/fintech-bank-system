from django.urls import path
from . import views

urlpatterns = [
    path('', views.role_select, name='role_select'),
]