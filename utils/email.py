from django.conf.urls.static import settings
from django.core.mail import send_mail,EmailMessage
from django.utils import timezone
from account.models import Verification,ResetVerification
import random
def generate_verification(user):
    generated_code = random.randint(100000,1000000)
    while Verification.objects.filter(code=generated_code):
        generated_code = random.randint(100000,1000000)
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


def generate_reset_verification(user):
    for v in ResetVerification.objects.filter(user=user):
        v.delete()
    generated_code = random.randint(100000,1000000)
    while ResetVerification.objects.filter(code=generated_code):
        generated_code = random.randint(100000,1000000)
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

def send_verify_request_to_admin(subject,message):
    to = 'trigger7701@gmail.com' if settings.DEBUG else settings.EMAIL_HOST_USER
    print(to)
    email = EmailMessage(subject=subject, body=message, to=[to])
    email.send()