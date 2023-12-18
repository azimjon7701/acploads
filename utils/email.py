import random

from django.conf.urls.static import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.html import format_html

from account.models import Verification, ResetVerification
from any_cap.settings import get_current_url


def generate_verification(user):
    generated_code = random.randint(100000, 1000000)
    while Verification.objects.filter(code=generated_code):
        generated_code = random.randint(100000, 1000000)
    verify = Verification.objects.create(
        user=user,
        code=generated_code,
        expired_date=timezone.now() + timezone.timedelta(minutes=10)
    )
    subject = "Verification code!"
    message = f"Your verification code: {verify.code}"
    if user.email:
        email = EmailMessage(subject=subject, body=message, to=[user.email])
        email.send()

    return verify


def generate_verification_url(user):
    generated_code = random.randint(100000, 1000000)
    while Verification.objects.filter(code=generated_code):
        generated_code = random.randint(100000, 1000000)
    verify = Verification.objects.create(
        user=user,
        code=generated_code,
        expired_date=timezone.now() + timezone.timedelta(minutes=10)
    )
    subject = "Verification!"
    message = format_html(
        f"""Click the link to confirm your account.<br> Verification url: {get_current_url()}auth/verify-account/?key={verify.code}""")
    if user.email:
        email = EmailMessage(subject=subject, body=message, to=[user.email])
        email.content_subtype = "html"
        email.send()

    return verify


def generate_reset_verification(user):
    for v in ResetVerification.objects.filter(user=user):
        v.delete()
    generated_code = random.randint(100000, 1000000)
    while ResetVerification.objects.filter(code=generated_code):
        generated_code = random.randint(100000, 1000000)
    verify = ResetVerification.objects.create(
        user=user,
        code=generated_code,
        expired_date=timezone.now() + timezone.timedelta(minutes=10)
    )
    subject = "Verification code to change password!"
    message = f"Your verification code: {verify.code}"
    if user.email:
        email = EmailMessage(subject=subject, body=message, to=[user.email])
        email.send()

    return verify


def send_verify_request_to_admin(subject, message):
    to = 'trigger7701@gmail.com' if settings.DEBUG else settings.EMAIL_HOST_USER
    email = EmailMessage(subject=subject, body=message, to=[to])
    email.send()
