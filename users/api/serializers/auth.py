from rest_framework import serializers


class EndWorkerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})


class EndWorkerRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'})


class EndWorkerTokenLoginSerializer(serializers.Serializer):
    token = serializers.CharField(allow_null=True)


class EndWorkerEmailInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EndWorkerUsernameInfoSerializer(serializers.Serializer):
    username = serializers.CharField()
