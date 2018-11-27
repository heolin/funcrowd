from rest_framework import serializers

from tasks.models import ItemTemplate, ItemTemplateField


class ItemTemplateFieldSerializer(serializers.ModelSerializer):
    data_source = serializers.CharField(source='data_source.name', allow_null=True)

    class Meta:
        model = ItemTemplateField
        fields = ('id', 'name', 'editable', 'required', 'data_source', "widget", "feedback")


class ItemTemplateSerializer(serializers.ModelSerializer):
    fields = ItemTemplateFieldSerializer(many=True, read_only=True)

    class Meta:
        model = ItemTemplate
        fields = ('id', 'name', 'fields')
