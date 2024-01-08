from rest_framework.routers import DefaultRouter
from main.api_views.carrier_dispatcher_views import search_view, load_view

carrier_dispatcher_router = DefaultRouter()
carrier_dispatcher_router.register(r'search', search_view.SearchViewSet, basename='Search')
carrier_dispatcher_router.register(r'load', load_view.LoadViewSet, basename='Load')