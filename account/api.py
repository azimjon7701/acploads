from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account import api_views

router = DefaultRouter()
router.register(r'check-email', api_views.EmailCheckViewSet, basename='email-check')
router.register(r'check-phone', api_views.PhoneCheckViewSet, basename='check-phone')
router.register(r'register', api_views.RegisterViewSet, basename='register')
router.register(r'verify-account', api_views.VerificationViewSet, basename='verify-account')
router.register(r'login', api_views.LoginViewSet, basename='login')