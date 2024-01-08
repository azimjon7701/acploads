from rest_framework import serializers

from main.models import LoadType, LoadTypeCategory


class LoadTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadType
        fields = ['id', 'name']


class LoadTypeCategorySerializer(serializers.ModelSerializer):
    types = LoadTypeSerializer(many=True, read_only=True)

    class Meta:
        model = LoadTypeCategory
        fields = ['id', 'name', 'types']
