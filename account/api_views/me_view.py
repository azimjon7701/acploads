from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account import serializers, models
from utils.authentication import get_current_user


class MyProfileViewSet(GenericViewSet, ListModelMixin):
    serializer_class = serializers.MeSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_data = get_current_user()
        serializer = serializers.MeSerializer(user_data, many=False)
        return Response(serializer.data)
