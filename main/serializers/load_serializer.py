from rest_framework import serializers

from main.models import LoadType, Load

class CListField(serializers.ListField):
    def get_value(self, value):
        print(value)
        return super().get_value(value)

    def to_representation(self, data):
        instance:Load = data.instance
        types = instance.type.all()
        print(types)
        if types is not None and len(types) > 0:
            return [item.id for item in types]
        else:
            return []


class LoadTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadType
        fields = '__all__'

class LoadSerializer(serializers.ModelSerializer):
    type = LoadTypeSerializer(many=True, read_only=True)
    class Meta:
        model = Load
        fields = [
            'id',
            'origin',
            'dh_o',
            'destination',
            'dh_d',
            'distance',
            'pickup_date',
            'age',
            'length',
            'weight',
            'dlv_date',
            'ref_number',
            'commodity',
            'price',
            'type_operator',
            'type',
            'truck_status',
            'name',
            'contact_type',
            'contact',
            'comment'
        ]

class LoadInputSerializer(serializers.Serializer):
    origin = serializers.CharField()
    dh_o = serializers.FloatField()
    destination = serializers.CharField(required=False)
    dh_d = serializers.FloatField(required=False)
    distance = serializers.FloatField(required=False)
    pickup_date = serializers.DateField()
    age = serializers.IntegerField()
    length = serializers.FloatField()
    weight = serializers.FloatField()
    dlv_date = serializers.DateField(required=False)
    ref_number = serializers.CharField(required=False)
    commodity = serializers.CharField(required=False)
    price = serializers.FloatField(required=False)
    type_operator = serializers.CharField(required=False)
    type = CListField(child=serializers.IntegerField())
    truck_status = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    contact_type = serializers.CharField(required=False)
    contact = serializers.CharField(required=False)
    comment = serializers.CharField(required=False)
