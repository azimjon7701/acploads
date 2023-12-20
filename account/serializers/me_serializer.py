from rest_framework import serializers


class MeSerializer(serializers.Serializer):
    entity_type = serializers.ChoiceField(choices=['carrier', 'broker', 'shipper'], required=True)
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False)
    mc = serializers.IntegerField(required=False)
    usdot = serializers.IntegerField(required=False)
    company_name = serializers.CharField(max_length=200, required=False)
    company_address = serializers.CharField(max_length=200, required=False)
    company_phone = serializers.CharField(max_length=20, required=False)

    def validate_phone(self, value):
        if not value.startswith('+') or not value[1:].isdigit():
            raise serializers.ValidationError("Invalid phone number format: phone")
        return value

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords don't match")
        return data
