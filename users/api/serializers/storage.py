from rest_framework import serializers

from users.models.storage import Storage


class StorageGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage
        fields = ('user', 'key', 'data')


class StoragePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage
        fields = ('data', )


class StorageBatchPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage
        fields = ('data', 'key')
