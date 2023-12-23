from rest_framework import serializers
from main.models import LoadType

class LoadTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadType
        fields = '__all__'
