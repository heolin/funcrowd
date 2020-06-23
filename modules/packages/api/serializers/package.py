from rest_framework import serializers

from modules.packages.models import Package
from tasks.api.serializers.item import ItemSerializer


class PackageSerializer(serializers.ModelSerializer):
    instruction = serializers.CharField(source='parent.instruction')

    class Meta:
        model = Package
        fields = ('id', 'order', 'metadata', 'status', 'name', 'instruction')


class PackageItemsSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ('id', 'items', 'order', 'metadata', 'status', 'name')


class CreatePackageSerializer(serializers.Serializer):
    size = serializers.IntegerField(required=True)
    metadata = serializers.DictField(default={})
