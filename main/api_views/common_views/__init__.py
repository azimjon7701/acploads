from rest_framework.routers import DefaultRouter
from main.api_views.common_views import load_type_view

common_router = DefaultRouter()
common_router.register(r'load-type', load_type_view.LoadTypeReadOnlyViewSet, basename='load-type')
common_router.register(r'load-type-category', load_type_view.LoadTypeCategoryReadOnlyViewSet, basename='load-type-category')