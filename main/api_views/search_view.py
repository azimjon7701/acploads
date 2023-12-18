from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from main import models
from main.models import Search
from main.serializers import SearchSerializer
from utils.authentication import AuthTokenAuthentication


class SearchViewSet(viewsets.ModelViewSet):
    serializer_class = SearchSerializer
    queryset = models.Search.objects.all()
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        query = Q(owner=user.profile)
        queryset = self.queryset.filter(query)
        return queryset

    def list(self, request, *args, **kwargs):
        user = self.request.user
        return super(SearchViewSet, self).list(request, *args, **kwargs)
