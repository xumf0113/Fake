# encoding: utf-8
import re

from django import forms
from django.core.validators import ValidationError

from .models import UserProfile


class FormTable(forms.Form):
    username = forms.CharField(min_length=5, max_length=20, label='用户名',
                               error_messages={'min_length': '请输入5-20个字符的用户名'})
    password = forms.CharField(min_length=6, max_length=20, required=True, error_messages={'required': '密码不能为空',
                                                                                           'min_length': '密码不能少于6位',
                                                                                           'max_length': '密码最多50位'})
    email = forms.CharField(required=True, error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    mobile = forms.CharField(required=True, error_messages={'required': '手机号不能为空', 'invalid': '邮箱格式错误'})
