import pytest
from jsonschema import ValidationError

from tasks.models import ItemTemplate


@pytest.fixture
def item_template_schema_no_fields():
    return {
        "name": "test",
        "fields": []
    }


@pytest.mark.django_db
def test_create_template_from_schema_no_fields(item_template_schema_no_fields):
    schema = item_template_schema_no_fields

    with pytest.raises(ValidationError):
        ItemTemplate.create_template_from_schema(schema)


@pytest.mark.parametrize(
    "item_template_schema",
    [
        {
            "name": "test1",
            "fields": [
                {"name": "field1", "widget": "TextLabel"}
            ]
        },
        {
            "name": "test2",
            "fields": [
                {
                    "name": "field1",
                    "widget": "TextLabel",
                    "required": False,
                    "feedback": False
                },
                {
                    "name": "field2",
                    "widget": "ChoiceField",
                    "required": True,
                    "editable": False,
                    "feedback": True,
                    "data_source": "sourceField"
                },
                {
                    "name": "sourceField",
                    "widget": "Hidden"
                }
            ]
        }
    ]
)
@pytest.mark.django_db
def test_create_template_from_schema(item_template_schema):
    schema = item_template_schema

    ItemTemplate.create_template_from_schema(schema)

    item_template = ItemTemplate.objects.get(name=schema['name'])
    assert item_template is not None
    assert item_template.fields.count() == len(schema['fields'])

    for field in schema['fields']:
        template_field = item_template.fields.get(name=field['name'])
        assert template_field is not None
        assert template_field.widget == field['widget']
