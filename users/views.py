import re
from datetime import datetime

import django_redis
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.core.validators import ValidationError

from .models import UserProfile
from .forms import FormTable


class CheckUsernameView(View):
    """登陆页面用户名鼠标移除事件检查用户名存在性"""

    def post(self, request):
        username = request.POST.get('username')
        if username:  # 如果能够从前端输入框获取到内容
            user = UserProfile.objects.filter(username=username).first()
            if user:  # 如果有用户
                return JsonResponse({'error': '1', 'msg': '用户名已经存在'})
            else:  # 如果没有当前用户
                return JsonResponse({'error': '0', 'msg': 'ok'})
        else:
            return JsonResponse({'error': '1', 'msg': '请输入用户名'})


class CheckMobile(View):
    """检查手机号"""

    def post(self, request):
        mobile = request.POST.get('mobile')
        if mobile:  # 如果能够从前端输入框获取到内容
            ret = re.match(r'^1[345789]\d{9}$', mobile)
            if ret:
                user = UserProfile.objects.filter(mobile=mobile).first()
                if user:  # 如果有用户
                    return JsonResponse({'error': '1', 'msg': '手机号已经存在'})
                else:  # 如果没有当前用户
                    return JsonResponse({'error': '0', 'msg': 'ok'})
            else:
                return JsonResponse({'error': '1', 'msg': '请输入正确的手机号'})
        else:
            return JsonResponse({'error': '1', 'msg': '请输入手机号'})


class SignupView(View):
    """注册提交页面"""

    def get(self, request):
        return render(request, 'user/signup.html')

    def post(self, request):
        has_error = True
        obj = FormTable(request.POST)
        if obj.is_valid():
            has_error = False
            username = obj.cleaned_data.get('username')
            password = obj.cleaned_data.get('password')
            email = obj.cleaned_data.get('email')
            mobile = obj.cleaned_data.get('mobile')
            user = UserProfile()
            user.username = username
            user.set_password = password
            user.email = email
            user.mobile = mobile
            user.save()
            return render(request, 'user/signin.html')
        else:
            return render(request, 'user/signup.html', locals())  # TODO 我可以直接把所有的数据放这里，　不用传递ＪＳＯＮ数据了


class SigninView(View):
    """登陆页面"""

    def get(self, request):
        return render(request, 'user/signin.html')

    def post(self, request):
        has_error = True
        sms_code = request.POST.get('check_code', None)
        if sms_code:
            # # 如果有验证码，　就和redis当中的进行验证
            # redis_conn = django_redis.get_redis_connection('verify')
            #
            # # 先从数据库当中取验证码
            # real_sms_code = redis_conn.get('sms_code')
            # if sms_code.upper() != real_sms_code.decode().upper():
            #     code_error = '验证码错误'
            #
            # print(request.POST.get('checkCode'))
            obj = FormTable(request.POST)
            if obj.is_valid():
                username = obj.cleaned_data.get('username')
                password = obj.cleaned_data.get('password')
                user = UserProfile.objects.filter(Q(username=username) | Q(email=username)).first()
                if user:
                    if user.check_password(password):
                        user.last_login = datetime.now()
                        request.session['user_id'] = user.id
                        print(request.session.session_key)
                    else:
                        user_error = '用户名或密码错误'
                else:
                    user_error = '用户不存在'
        else:
            code_error = '验证码不能为空'
        return render(request, 'user/signin.html', locals())


class SignoutView(View):
    """退出页面"""

    def post(self, request):
        return render(request, 'user/signout.html')
