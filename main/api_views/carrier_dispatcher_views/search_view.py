from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main import models
from main.models import Search, LoadType
from main.serializers import SearchSerializer
from main.serializers.search_serializer import SearchInputSerializer


class SearchViewSet(viewsets.ModelViewSet):
    serializer_class = SearchSerializer
    queryset = models.Search.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return SearchInputSerializer
        return SearchSerializer

    def get_queryset(self):
        user = self.request.user
        query = Q(owner=user.profile)
        queryset = self.queryset.filter(query)
        return queryset

    def perform_create(self, serializer):
        search = Search.objects.create(
            owner=self.request.user.profile,
            age=serializer.validated_data.get('age'),
            pickup_date=serializer.validated_data.get('pickup_date'),
            origin=serializer.validated_data.get('origin'),
            dh_o=serializer.validated_data.get('dh_o'),
            destination=serializer.validated_data.get('destination'),
            dh_d=serializer.validated_data.get('dh_d'),
            distance=serializer.validated_data.get('distance'),
            length=serializer.validated_data.get('length'),
            weight=serializer.validated_data.get('weight'),
            type_operator=serializer.validated_data.get('type_operator')
        )
        types = LoadType.objects.filter(id__in=serializer.validated_data.get('types', []))
        for type in types:
            search.type.add(type)
