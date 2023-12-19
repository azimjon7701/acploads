from django.db import transaction
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account import serializers, models
from account.models import generate_rand_username
from utils.email import generate_verification_url
from utils.services.fmcsa_service import get_fmcsa_data


class RegisterViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = serializers.RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mc = serializer.validated_data.get('mc')
        usdot = serializer.validated_data.get('usdot')
        try:
            with transaction.atomic():
                if mc is None and usdot is None:
                    self.__create_carrier_dispatcher(
                        validated_data=serializer.validated_data
                    )
                else:
                    self.__create_verified_member(
                        validated_data=serializer.validated_data
                    )

        except Exception as e:
            print('Exception: ', e)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def __create_carrier_dispatcher(self, validated_data: dict):
        entity_type = validated_data.get('entity_type')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        phone = validated_data.get('phone')
        password = validated_data.get('password')
        company_name = validated_data.get('company_name')
        company_address = validated_data.get('company_address')
        company_phone = validated_data.get('company_phone')
        user = models.User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=generate_rand_username(),
            email=email,
            is_active=False
        )
        user.set_password(password)
        user.save()
        profile = models.Profile.objects.create(
            user=user,
            phone=phone
        )
        profile.generate_customer_id()
        company = models.Company.objects.create(
            name=company_name,
            address1=company_address,
            entity_type=entity_type,
            phone=company_phone
        )
        company_employee = models.CompanyEmployee.objects.create(
            company=company,
            employee=profile
        )
        generate_verification_url(user=user)

    def __create_verified_member(self, validated_data: dict):
        entity_type = validated_data.get('entity_type')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        phone = validated_data.get('phone')
        password = validated_data.get('password')
        mc = validated_data.get('mc')
        usdot = validated_data.get('usdot')
        company_data = {}
        if mc:
            company_data = get_fmcsa_data(
                query_param='MC_MX',
                query_string=mc
            )
        elif usdot:
            company_data = get_fmcsa_data(
                query_param='USDOT',
                query_string=usdot
            )
        if 'error' in company_data:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("mc or usdot data")
        user = models.User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=generate_rand_username(),
            email=email,
            is_active=False
        )
        user.set_password(password)
        user.save()
        profile = models.Profile.objects.create(
            user=user,
            phone=phone
        )
        profile.generate_customer_id()
        company = models.Company.objects.create(
            entity_type=entity_type,
            mc=company_data.get('mc_mx_ff_numbers'),
            usdot=company_data.get('usdot_number'),
            name=company_data.get('legal_name'),
            dba_name=company_data.get('dba_name'),
            address1=company_data.get('physical_address'),
            address2=company_data.get('mailing_address'),
            phone=company_data.get('phone')
        )
        company_employee = models.CompanyEmployee.objects.create(
            company=company,
            employee=profile
        )
        generate_verification_url(user=user)