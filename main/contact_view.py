from django.core.mail import EmailMessage
from django.shortcuts import redirect

from main.models import ContactUs


def contact_us_form(request):
    if request.POST:
        name: str = request.POST.get("name", None)
        email: str = request.POST.get("email", None)
        phone: str = request.POST.get("phone", None)
        comment: str = request.POST.get("comment", None)
        try:
            contact_us = ContactUs.objects.create(
                name=name,
                email=email,
                phone=phone,
                comment=comment
            )
            email = EmailMessage(subject='Message From Anycappro.com', body=contact_us.message(),
                                 to=['nodir-70@bk.ru', 'anycappro@gmail.com'])
            email.send()
            return redirect('/account/?alert=1')
        except:
            pass
    return redirect('account')

def contact_us_form_footer(request):
    if request.POST:
        name: str = request.POST.get("name", None)
        email: str = request.POST.get("email", None)
        phone: str = request.POST.get("phone", None)
        comment: str = request.POST.get("comment", None)
        try:
            contact_us = ContactUs.objects.create(
                name=name,
                email=email,
                phone=phone,
                comment=comment
            )
            email = EmailMessage(subject='Message From Anycappro.com', body=contact_us.message(),
                                 to=['nodir-70@bk.ru', 'anycappro@gmail.com'])
            email.send()
            return redirect('/?alert=1')
        except:
            pass
    return redirect('account')


def contact_us_form_contact_page(request):
    if request.POST:
        name: str = request.POST.get("name", None)
        email: str = request.POST.get("email", None)
        phone: str = request.POST.get("phone", None)
        comment: str = request.POST.get("comment", None)
        try:
            contact_us = ContactUs.objects.create(
                name=name,
                email=email,
                phone=phone,
                comment=comment
            )
            email = EmailMessage(subject='Message From Anycappro.com', body=contact_us.message(),
                                 to=['nodir-70@bk.ru', 'anycappro@gmail.com'])
            email.send()
            return redirect('/contact-us/?alert=1')
        except:
            pass
    return redirect('account')
