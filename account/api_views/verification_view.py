from django.utils import timezone
from rest_framework import status
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account import serializers
from account.models import Verification


class VerificationViewSet(GenericViewSet, ListModelMixin):
    serializer_class = serializers.LoginSerializer

    def list(self, request, *args, **kwargs):
        verification_key = self.request.query_params.get('key')
        if verification_key is None:
            return Response(
                data={'message': 'Verification key required'}, status=status.HTTP_400_BAD_REQUEST
            )
        if Verification.objects.filter(code=verification_key).exists():
            verify = Verification.objects.filter(code=verification_key).first()
            if verify.code == verification_key and verify.expired_date > timezone.now():
                verify.user.is_active = True
                verify.user.save()
                return Response(
                    data={'message': 'Successfully verified!'}, status=status.HTTP_200_OK
                )
        return Response(
                data={'message': 'Not verified'}, status=status.HTTP_400_BAD_REQUEST
            )

