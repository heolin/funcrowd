# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import jsonschema
from django.db import models
from sortedm2m.fields import SortedManyToManyField

from tasks.models.template.item_template_field import ItemTemplateField
from tasks.models.template.schema import TEMPLATE_SCHEMA


class ItemTemplate(models.Model):
    """
    Provides information about fields, which makes an item's data.
    ItemTemplate decides among others: which fields are required, which are readonly,
    for which feedback will be generated, or which widget should they use in the frontend.
    """

    name = models.CharField(max_length=100, unique=True)
    fields = SortedManyToManyField("ItemTemplateField", related_name="template")

    def __str__(self):
        return "{}".format(self.name)

    @property
    def annotations_fields(self):
        """Read and write fields"""
        return self.fields.filter(editable=True)

    @property
    def feedback_fields(self):
        """Read and write fields with enabled feedback"""
        return self.annotations_fields.filter(feedback=True)

    @property
    def items_fields(self):
        """Read only fields"""
        return self.fields.filter(editable=False)

    @staticmethod
    def create_template_from_schema(schema):
        """
        Creates ItemTemplate and its corresponding ItemTemplateField
        based on a schema provided in a json form.

        :param schema: schema created according to appropriate schema
        :return:
        """
        jsonschema.validate(schema, TEMPLATE_SCHEMA)

        item_template = ItemTemplate.objects.create(name=schema['name'])

        fields = {}
        for field_template in schema['fields']:
            field = ItemTemplateField.objects.create(name=field_template['name'])
            item_template.fields.add(field)
            fields[field_template['name']] = field

        for field_template in schema['fields']:
            field = fields[field_template['name']]
            for key, value in field_template.items():
                if key == "name":
                    continue
                if key == "data_source":
                    field.data_source = fields[value]
                else:
                    setattr(field, key, value)
            field.save()

        return item_template
