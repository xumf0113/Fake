# encoding: utf-8
import re

from .models import UserProfile
from django import forms
from django.core.validators import ValidationError


def username_validate(value):
    """对登录的用户名进行校验"""
    # 取反的正则来匹配，　只要用户名里面有不满足的，　就抛出错误
    username_re = re.match(r'\W|[A-Z]', value)
    if username_re:
        raise ValidationError('用户名格式错误，　只能在[a-z][0-9]中选择')

    user = UserProfile.objects.filter(username=value)
    if user:
        raise ValidationError('用户名已经存在，　请换一个')


def mobile_validate(value):
    """对登录的手机号进行校验"""
    mobile_re = re.match(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$', value)
    if not mobile_re:
        raise ValidationError('手机号格式错误')

    user = UserProfile.objects.filter(mobile=value)
    if user:
        raise ValidationError('手机号已经存在，　请换一个')


def email_validate(value):
    """对登录的邮箱进行校验"""
    email_re = re.match(r'[0-9a-zA-Z_]{0,19}@(163|qq|126).com', value)
    if not email_re:
        raise ValidationError('邮箱格式错误')

    user = UserProfile.objects.filter(email=value).first()
    if user:
        raise ValidationError('邮箱已经存在，　请换一个')


class FormTable(forms.Form):
    username = forms.CharField(validators=[username_validate], min_length=5, max_length=20, label='用户名',
                               error_messages={'min_length': '请输入5-20个字符的用户名'})
    password = forms.CharField(min_length=6, max_length=20, required=True, error_messages={'required': '密码不能为空',
                                                                                           'min_length': '密码不能少于6位',
                                                                                           'max_length': '密码最多50位'})
    email = forms.CharField(validators=[email_validate], required=True, error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    mobile = forms.CharField(validators=[mobile_validate], required=True, error_messages={'required': '手机号不能为空', 'invalid': '邮箱格式错误'})
