# encoding: utf-8
from django.urls import path
from . import views

urlpatterns = [
    path(r'signup/', views.SignupView.as_view(), name='signup'),
    path(r'signin/', views.SigninView.as_view(), name='signin'),
    path(r'signout/', views.SignupView.as_view(), name='signout'),
    path(r'check_username/', views.CheckUsernameView.as_view()),
    path(r'check_mobile/', views.CheckMobile.as_view()),
]