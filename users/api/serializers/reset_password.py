from rest_framework import serializers


class ResetPasswordTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    password1 = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'})


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(style={'input_type': 'email'})
