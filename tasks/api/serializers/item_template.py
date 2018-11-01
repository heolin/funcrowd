from rest_framework import serializers

from tasks.models import ItemTemplate, ItemTemplateField


class ItemTemplateFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemTemplateField
        fields = ('id', 'name', 'editable', 'required', 'data_source', "widget")


class ItemTemplateSerializer(serializers.ModelSerializer):
    fields = ItemTemplateFieldSerializer(many=True, read_only=True)

    class Meta:
        model = ItemTemplate
        fields = ('id', 'name', 'fields')
