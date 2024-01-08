from django.urls import path, include

from main.api_views import common_views, carrier_dispatcher_views

urlpatterns = [
    path('common/', include(common_views.common_router.urls)),
    path('carrier-dispatcher/', include(carrier_dispatcher_views.carrier_dispatcher_router.urls))
]
