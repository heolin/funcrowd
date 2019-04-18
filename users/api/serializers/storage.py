from rest_framework import serializers

from users.models.storage import Storage


class StorageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage
        fields = ('key', 'data')


class StoragePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage
        fields = ('data', )
