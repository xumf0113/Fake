import logging
import django_redis
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.core.validators import ValidationError

from utils.captcha.captcha import captcha
from . import constants

logger = logging.getLogger('django')


def get_code(request):
    text, image = captcha.generate_captcha()
    redis_conn = django_redis.get_redis_connection('verify')
    redis_conn.setex('sms_code', constants.IMAGE_CODE_REDIS_EXPIRES, text)
    return HttpResponse(image)


class CheckCodeView(View):
    def post(self, request):
        sms_code = request.POST.get('sms_code')
        if not sms_code:  # 如果没拿到验证码
            return JsonResponse({'error': 1, 'msg': '请填写验证码'})

        # 如果有验证码，　就和redis当中的进行验证
        redis_conn = django_redis.get_redis_connection('verify')

        # 先从数据库当中取验证码
        real_sms_code = redis_conn.get('sms_code')

        try:
            redis_conn.delete('sms_code')
        except Exception as e:
            logging.error(e)

        if real_sms_code is None:
            return JsonResponse({'error': 1, 'msg': '请刷新验证码'})

        if sms_code.upper() != real_sms_code.decode().upper():
            return JsonResponse({'error': 1, 'msg': '验证码不正确'})

        return JsonResponse({'error': 0, 'msg': 'ok'})
