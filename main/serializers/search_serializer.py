from rest_framework import serializers

from main.models import Search, LoadType


class LoadTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadType
        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    type = LoadTypeSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.id')
    pickup_date_for_picker = serializers.DateField(source='pickup_date', format='%Y-%m-%d', required=False,
                                                   read_only=True)
    results_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Search
        fields = [
            'id',
            'owner',
            'age',
            'pickup_date',
            'pickup_date_for_picker',
            'origin',
            'dh_o',
            'destination',
            'dh_d',
            'distance',
            'length',
            'weight',
            'type_operator',
            'type',
            'truck_status',
            'notification_status',
            'results_count'
        ]


class SearchInputSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    types = serializers.ListSerializer(child=serializers.IntegerField(write_only=True))

    class Meta:
        model = Search
        fields = [
            'id',
            'owner',
            'age',
            'pickup_date',
            'origin',
            'dh_o',
            'destination',
            'dh_d',
            'distance',
            'length',
            'weight',
            'type_operator',
            'types',
            'truck_status',
            'notification_status'
        ]
