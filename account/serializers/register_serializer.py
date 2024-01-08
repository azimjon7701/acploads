from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    entity_type = serializers.ChoiceField(choices=['carrier_dispatcher','carrier', 'broker', 'shipper'], required=True)
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False)
    password = serializers.CharField(max_length=250, write_only=True)
    confirm_password = serializers.CharField(max_length=250, write_only=True)
    mc = serializers.CharField(max_length=20,required=False)
    usdot = serializers.CharField(max_length=20, required=False)
    company_name = serializers.CharField(max_length=200, required=False)
    company_address = serializers.CharField(max_length=200, required=False)
    company_phone = serializers.CharField(max_length=20, required=False)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords don't match")
        return data
