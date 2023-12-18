"""any_cap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static, settings
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from account import api as account_api
from main import api as main_api

schema_view = get_swagger_view(title='Your API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main.urls")),
    path('auth/', include(account_api.router.urls)),
    path('api/', include(main_api.router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
