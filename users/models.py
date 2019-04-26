from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户表
    """
    GENDER_TYPE = (
        ("male", "男"),
        ("female", "女"),
    )

    STATUS_TYPE = (
        ('ONLINE', "在线"),
        ('OFFLINE', "离线")
    )

    VERIFY_STATUS = (
        (0, "未验证"),
        (1, "已验证")
    )
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=GENDER_TYPE, default="female", verbose_name="性别")
    location = models.CharField(max_length=30, null=True, blank=True, default="", verbose_name="所在城市")
    mobile = models.CharField(max_length=11, null=True, blank=True, default="", verbose_name="电话")
    email = models.CharField(max_length=100, null=True, blank=True, default="", verbose_name="邮箱")
    email_verify = models.IntegerField(choices=VERIFY_STATUS, default=0, verbose_name="Email是否已经验证")
    mobile_verify = models.IntegerField(choices=VERIFY_STATUS, default=0, verbose_name="Mobile是否已经验证")
    avatar = models.CharField(max_length=50, null=True, blank=True, default="/static/img/default-avatar.png",
                              verbose_name="头像")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
