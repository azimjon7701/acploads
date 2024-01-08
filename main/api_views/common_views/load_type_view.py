# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from main.models import LoadTypeCategory, LoadType
from main.serializers import LoadTypeCategorySerializer, LoadTypeSerializer


class LoadTypeReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LoadType.objects.all()
    serializer_class = LoadTypeSerializer
    permission_classes = [IsAuthenticated]


class LoadTypeCategoryReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LoadTypeCategory.objects.all()
    serializer_class = LoadTypeCategorySerializer
    permission_classes = [IsAuthenticated]
