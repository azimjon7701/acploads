from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from main import models
from main.models import Load, LoadType
from main.serializers import LoadSerializer, LoadInputSerializer


class LoadViewSet(viewsets.ModelViewSet):
    serializer_class = LoadSerializer
    queryset = models.Load.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return LoadInputSerializer
        return LoadSerializer

    # def get_serializer(self, *args, **kwargs):
    #     serializer_class = self.get_serializer_class()
    #     kwargs.setdefault('context', self.get_serializer_context())
    #     if serializer_class == LoadInputSerializer:
    #         instance:Load = kwargs.get('instance')
    #         if instance is None:
    #             return LoadInputSerializer()
    #         else:
    #             return LoadInputSerializer(
    #                 origin=instance.origin,
    #                 dh_o=instance.dh_o,
    #                 destination=instance.destination,
    #                 dh_d=instance.dh_d,
    #                 distance=instance.distance,
    #                 pickup_date=instance.pickup_date,
    #                 age=instance.age,
    #                 length=instance.length,
    #                 weight=instance.weight,
    #                 dlv_date=instance.dlv_date,
    #                 ref_number=instance.ref_number,
    #                 commodity=instance.commodity,
    #                 price=instance.price,
    #                 type_operator=instance.type_operator,
    #                 truck_status=instance.truck_status,
    #                 name=instance.name,
    #                 contact_type=instance.contact_type,
    #                 contact=instance.contact,
    #                 comment=instance.comment
    #             )
    #     return serializer_class(*args, **kwargs)

    # def get_queryset(self):
    #     user = self.request.user
    #     query = Q(owner=user.profile)
    #     queryset = self.queryset.filter(query)
    #     return queryset

    def perform_create(self, serializer):
        load = Load.objects.create(
            owner=self.request.user.profile,
            origin=serializer.validated_data.get('origin'),
            dh_o=serializer.validated_data.get('dh_o'),
            destination=serializer.validated_data.get('destination'),
            dh_d=serializer.validated_data.get('dh_d'),
            distance=serializer.validated_data.get('distance'),
            pickup_date=serializer.validated_data.get('pickup_date'),
            age=serializer.validated_data.get('age'),
            length=serializer.validated_data.get('length'),
            weight=serializer.validated_data.get('weight'),
            dlv_date=serializer.validated_data.get('dlv_date'),
            ref_number=serializer.validated_data.get('ref_number'),
            commodity=serializer.validated_data.get('commodity'),
            price=serializer.validated_data.get('price'),
            type_operator=serializer.validated_data.get('type_operator'),
            truck_status=serializer.validated_data.get('truck_status'),
            name=serializer.validated_data.get('name'),
            contact_type=serializer.validated_data.get('contact_type'),
            contact=serializer.validated_data.get('contact'),
            comment=serializer.validated_data.get('comment')
        )
        types = LoadType.objects.filter(id__in=serializer.validated_data.get('type', []))
        for type in types:
            load.type.add(type)
