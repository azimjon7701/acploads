from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account import models, serializers


class EmailCheckViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = serializers.EmailCheckSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = models.User.objects.filter(email=email).exists()
        if not user:
            return Response(
                data={'message': 'Email not used'}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'message': 'Email already used'}, status=status.HTTP_400_BAD_REQUEST
            )


class PhoneCheckViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = serializers.PhoneCheckSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        user = models.Profile.objects.filter(phone=phone).exists()
        if not user:
            return Response(
                data={'message': 'Phone not used'}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'message': 'Phone already used'}, status=status.HTTP_400_BAD_REQUEST
            )
