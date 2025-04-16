from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class PhoneNumberSerializer(serializers.Serializer):
    """
    Serializer for phone number validation.
    """
    phone_number = serializers.CharField(max_length=11, required=True)

    def validate_phone_number(self, value):
        """
        Validate the phone number format.
        """
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits.")
        if len(value) != 11:
            raise serializers.ValidationError(
                "Phone number must be between 11 digits.")
        return value


class OTPSerializer(serializers.Serializer):
    """
    Serializer for OTP validation.
    """

    phone_number = serializers.CharField(max_length=11, required=True)
    otp = serializers.CharField(max_length=6, required=True)

    def validate_otp(self, value):
        """
        Validate the OTP format.
        """
        if not value.isdigit():
            raise serializers.ValidationError(
                "OTP must contain only digits.")
        if len(value) != 6:
            raise serializers.ValidationError(
                "OTP must be 6 digits long.")
        return value

    def validate_phone_number(self, value):
        """
        Validate the phone number format.
        """
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits.")
        if len(value) != 11:
            raise serializers.ValidationError(
                "Phone number must be between 11 digits.")
        return value


class SetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate_phone_number(self, value):
        """
        Validate the phone number format.
        """
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits.")
        if len(value) != 11:
            raise serializers.ValidationError(
                "Phone number must be between 11 digits.")
        return value


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate_phone_number(self, value):
        """
        Validate the phone number format.
        """
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits.")
        if len(value) != 11:
            raise serializers.ValidationError(
                "Phone number must be between 11 digits.")
        return value

    def validate_password(self, value):
        """
        Validate the password format.
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']
        read_only_fields = ['phone_number']
