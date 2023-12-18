from django.conf.urls.static import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from account.company_model import CompanyEmployee
from account.models import Profile, Verification, ResetVerification, Company, generate_rand_username
from any_cap.settings import get_current_url
from utils.email import generate_verification, generate_reset_verification, send_verify_request_to_admin



def custom_login(request, user):
    [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == str(user.id)]
    login(request, user)


def login_view(request):
    context = {
        'congrast': False,
        'changed': False,
        'error': ''
    }
    congrast = request.GET.get('congrast', None)
    if congrast:
        context['congrast'] = True
    changed = request.GET.get('changed', None)
    if changed:
        context['changed'] = True
    if request.user.id:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if email and password:
            try:
                userr = User.objects.get(email=email)
                user = authenticate(username=userr.username, password=password)
                if user:
                    custom_login(request, user)
                    return redirect('/?modal=opened', )
                else:
                    context['error'] = 'Wrong email or password!'
            except Exception as e:
                print(e)
        context['error'] = 'Wrong email or password!'
        # if context.get('error',None):
        #     return redirect('login')
    return render(request, 'auth/login.html', context=context)


def register_view(request):
    if request.user.id:
        return redirect('home')
    context = {
        'email_error': '',
        'error': '',
        'terms_error': '',
    }
    if request.POST:
        tab = request.POST.get('tab', None)
        first_name:str = request.POST.get('first_name', None)
        last_name:str = request.POST.get('last_name', None)
        email:str = request.POST.get('email', None)
        password:str = request.POST.get('password', None)
        password1:str = request.POST.get('password1', None)
        company_id:str = request.POST.get('company-id', None)
        company_id = company_id.upper() if company_id else None
        is_new_company = request.POST.get('is-new-company', None)
        print('is new company:', is_new_company)
        if User.objects.filter(email=email):
            context['email_error'] = 'This email already exist'
        elif password == password1:
            try:
                username = generate_rand_username()
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    is_active=False
                )
                if user:
                    customer = Profile.objects.create(
                        user=user
                    )
                    customer.generate_customer_id()
                    if tab == 'company' and company_id:
                        print("c_id", company_id)
                        companies = Company.objects.filter(company_id=company_id)
                        print("COMP:",companies)
                        if is_new_company == 'true':
                            company = Company.objects.create(
                                company_id=company_id.upper()
                            )
                            print(company)
                            company_employee = CompanyEmployee.objects.create(
                                company=company,
                                employee=customer,
                                is_owner=True
                            )
                            subject = "Create new user with company"
                            message = f"""User {customer} is asking to confirm his {company} company View in admin: {get_current_url()}admin/account/company/{company.id}/change/"""
                            send_verify_request_to_admin(subject, message)
                            print("send 1")
                        else:
                            company = companies.first()
                            print("companies:",companies)
                            print("company:",company)
                            if company:
                                company_employee = CompanyEmployee.objects.create(
                                    company=company,
                                    employee=customer
                                )
                                print(company)
                                subject = "Join new user to company"
                                message = f"""User {customer} is asking to confirm his membership in {company} <br>company View in admin: {get_current_url()}admin/account/company/{company.id}/change/"""
                                send_verify_request_to_admin(subject, message)
                                print("send 2")
                    verify = generate_verification(user=user)
                    return redirect(f'/confirmation/{user.id}')
            except Exception as e:
                print('Error:',e)
            context['error'] = 'Register not complated'

    return render(request, 'auth/register.html', context=context)


def confirmation_view(request, user_id):
    if request.user.id:
        return redirect('home')
    context = {'error': ''}
    if request.POST:
        confirmation: str = request.POST.get('confirmation', None)
        verify = Verification.objects.filter(code=confirmation) if confirmation.isdigit() else []
        if verify and confirmation:
            verification = verify[0]
            if verification.user_id == user_id and verification.expired_date > timezone.now():
                if confirmation == str(verification.code):
                    verification.user.is_active = True
                    verification.user.save()
                    return redirect('/login/?congrast=1')
        context['error'] = 'Confirmation not complated!'

    return render(request, 'auth/confirmation.html', context=context)


def logout_view(request):
    if request.user.id:
        logout(request)
    return redirect('login')


def forgot_password_view(request):
    if request.user.id:
        return redirect('home')
    if request.POST:
        email = request.POST.get('email', None)
        if email:
            users = User.objects.filter(email=email)
            if users:
                user = users[0]
                verify = generate_reset_verification(user=user)
                return redirect(f'/confirm-password/{user.id}')
    return render(request, 'auth/forgot_password.html')


@login_required
def profile_page_view(request):
    context = {
        'current_tab': 'details',
        'alert': False,
        'saved': False,
        'changed': False,
        'page_title': 'Profile Settings'
    }
    tab = request.GET.get('tab', None)
    alert = request.GET.get('alert', None)
    if alert:
        context['alert'] = True
    saved = request.GET.get('saved', None)
    if saved:
        context['saved'] = True
    changed = request.GET.get('changed', None)
    if changed:
        context['changed'] = True
    if tab == 'password':
        context['current_tab'] = 'password'
        context['error'] = 'Password reset failed!'
    return render(request, 'profile/profile.html', context=context)


@login_required
def scammers_list_view(request):
    context = {
        'page_title': 'Blocked Users List',
        'current_tab': 'details',
    }
    return render(request, 'profile/scammers_list.html', context=context)


@login_required
def find_users_view(request):
    search = request.GET.get('search', None)
    users = []
    if search:
        users = User.objects.filter(first_name__search=search)
    context = {
        'page_title': 'Find users',
        'current_tab': 'details',
        'users': users
    }
    return render(request, 'profile/find_user.html', context=context)


@login_required
def edit_profile_view(request):
    if request.POST:
        first_name: str = request.POST.get("first_name", None)
        last_name: str = request.POST.get("last_name", None)
        email: str = request.POST.get("email", None)
        telegram: str = request.POST.get("telegram", None)
        phone: str = request.POST.get("phone", None)
        user = request.user
        print(first_name, last_name, email, telegram, phone)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        user.save()
        if telegram:
            telegram = telegram if telegram.startswith('@') else '@' + telegram
            user.profile.telegram = telegram
        if phone:
            user.profile.phone = phone
        user.profile.save()
        return redirect('/account/?saved=1')

    return redirect('account')


@login_required
def password_reset_view(request):
    context = {'error': ''}
    if request.POST:
        current_password: str = request.POST.get("current-password", None)
        new_password: str = request.POST.get("new-password", None)
        confirm_password: str = request.POST.get("confirm-password", None)
        if current_password:
            user: User = authenticate(username=request.user.username, password=current_password)
            if user:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    custom_login(request, user)
                    return redirect('/account/?changed=1')

    return redirect('/account/?tab=password')


def confirm_password_view(request, user_id):
    if request.user.id:
        return redirect('home')
    context = {'error': ''}
    if request.POST:
        confirmation: str = request.POST.get('confirmation', None)
        new_password: str = request.POST.get('new-password', None)
        confirm_password: str = request.POST.get('confirm-password', None)
        verify = ResetVerification.objects.filter(code=confirmation) if confirmation.isdigit() else []
        if verify and confirmation:
            verification = verify[0]
            if verification.user_id == user_id and verification.expired_date > timezone.now():
                if new_password == confirm_password:
                    verification.user.set_password(new_password)
                    verification.user.save()
                    return redirect('/login/?changed=1')
        context['error'] = 'Confirmation failed!'
    return render(request, 'auth/confirm_password.html', context=context)


def terms_view(request):
    return render(request, 'auth/terms.html', context={'title': 'Terms and Services'})


def check_company_id(request):
    company = request.GET.get('company', None)
    if company:
        companies = Company.objects.filter(company_id=company)
        return JsonResponse({"avialable": bool(companies)})
    else:
        return JsonResponse(data={}, status=404)
