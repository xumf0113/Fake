import re

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
        obj = FormTable(request.POST)
        if obj.is_valid():
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
            return render(request, 'user/signin.html')


class SigninView(View):
    """登陆页面"""

    def post(self, request):
        return render(request, 'user/signin.html')


class SignoutView(View):
    """退出页面"""

    def post(self, request):
        return render(request, 'user/signout.html')
