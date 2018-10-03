from rest_framework import serializers

from tasks.models import Item
from tasks.api.serializers.item_template import ItemTemplateSerializer


class ItemSerializer(serializers.ModelSerializer):
    template = ItemTemplateSerializer(read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'task', 'data', 'template')
