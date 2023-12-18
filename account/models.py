import binascii
import os
import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from account.comment_models import *
from account.company_model import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telegram = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=30, null=True)
    customer_id = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)

    def generate_customer_id(self):
        self.customer_id = 10000 + self.id
        self.save()

    def __str__(self):
        if self.user.first_name:
            return self.user.first_name
        if self.user.last_name:
            return self.user.last_name
        if self.user.email:
            return self.user.email
        if self.user.username:
            return self.user.username
        return self.user.username


class Verification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField(unique=True)
    expired_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.email if self.user.email else self.code


class ResetVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField()
    expired_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.email if self.user.email else self.code


class AuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_tokens')
    key = models.CharField(max_length=40, unique=True, null=True)
    expired_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()

        if not self.expired_date:
            self.expired_date = timezone.now() + timedelta(days=3)
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()


def generate_rand_username():
    username = f'apc{random.randint(1000000, 10000000)}'
    while User.objects.filter(username=username).exists():
        username = f'apc{random.randint(1000000, 10000000)}'
    return username
