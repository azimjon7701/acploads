from rest_framework import serializers


class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class PhoneCheckSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)

    def validate_phone(self, value):
        if not value.startswith('+') or not value[1:].isdigit():
            raise serializers.ValidationError("Invalid phone number format")
        return value
