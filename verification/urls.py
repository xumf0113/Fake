# encoding: utf-8
from django.urls import path
from . import views

urlpatterns = [
    path(r'get_code/', views.get_code, name='get_code'),
    path(r'check_code/', views.CheckCodeView.as_view(), name='check_code'),
]
