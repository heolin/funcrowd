from rest_framework import serializers

from modules.packages.models import Package
from tasks.api.serializers.item import ItemSerializer


class PackageSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ('id', 'items', 'order')
