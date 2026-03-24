from django.urls import path
from . import views

urlpatterns = [
    path('withdraw/', views.withdraw_view),
]