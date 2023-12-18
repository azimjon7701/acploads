from rest_framework import serializers

from main.models import Search


class SearchSerializer(serializers.ModelSerializer):
    pickup_date_for_picker = serializers.DateField(source='pickup_date', format='%Y-%m-%d', required=False)
    type = serializers.CharField(source='type.name', required=False)

    class Meta:
        model = Search
        fields = [
            'id',
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
            'type',
        ]
