from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main import api_views

router = DefaultRouter()
router.register(r'search', api_views.SearchViewSet, basename='Search')
router.register(r'load-type', api_views.LoadTypeReadOnlyViewSet, basename='Load Type')