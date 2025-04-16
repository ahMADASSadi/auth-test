from datetime import timedelta
import random

from django.contrib.auth.models import AbstractBaseUser as BaseUser, PermissionsMixin
from django.utils import timezone
from django.db import models

from core.validators import PHONE_NUMBER_VALIDATOR
from core.managers import UserManager


class User(BaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=11, unique=True, null=False, blank=False, validators=[PHONE_NUMBER_VALIDATOR])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(
        max_length=255, unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.phone_number!r}"

    @property
    def is_admin(self):
        return self.is_superuser


class OTP(models.Model):
    COOLDOWN_TIME = timedelta(minutes=3)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self) -> bool:
        return self.created_at >= timezone.now() - self.COOLDOWN_TIME

    def generate_otp(self) -> str:
        return f"{random.randint(100000, 999999):06}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_otp()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"OTP for {self.user.phone_number!s} - Code: {self.code!r}"
