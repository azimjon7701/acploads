# views.py
from rest_framework import viewsets
from main.models import LoadType
from main.serializers import LoadTypeSerializer
from utils.permission_classes import IsCarrier


class LoadTypeReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LoadType.objects.all()
    serializer_class = LoadTypeSerializer
    permission_classes = [IsCarrier]
