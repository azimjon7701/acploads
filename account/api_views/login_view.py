from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account import models, serializers


class LoginViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = serializers.LoginSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user: models.User = models.User.objects.filter(email=email).first()
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                token, created = models.AuthToken.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
