import pytest

from tasks.models import ItemTemplate


@pytest.fixture
@pytest.mark.django_db
def item_template_one_input_one_output():
    """
    ItemTemplate for item with one input field, and one output field.
    """
    return ItemTemplate.create_template_from_schema({
        "name": "template",
        "fields": [
            {
                "name": "data_field",
                "widget": "TextLabel"
            },
            {
                "name": "input_field",
                "widget": "InputField",
                "editable": True,
                "feedback": True
            }
        ]
    })


@pytest.fixture
@pytest.mark.django_db
def item_template_one_input_one_output_data_source():
    return ItemTemplate.create_template_from_schema({
        """
        ItemTemplate for item with one input field,
        and one output field, that is using other field as data source.
        """
        "name": "template",
        "fields": [
            {
                "name": "data_field",
                "widget": "TextLabel"
            },
            {
                "name": "data_options",
                "widget": "Hidden"
            },
            {
                "name": "input_field",
                "widget": "InputField",
                "editable": True,
                "feedback": True,
                "data_source": "data_options"
            }
        ]
    })


@pytest.fixture
@pytest.mark.django_db
def item_template_one_input_two_output():
    """
    ItemTemplate for item with one input field, and two output fields.
    """
    return ItemTemplate.create_template_from_schema({
        "name": "template",
        "fields": [
            {
                "name": "data_field",
                "widget": "TextLabel"
            },
            {
                "name": "input_field1",
                "widget": "InputField",
                "editable": True,
                "feedback": True
            },
            {
                "name": "input_field2",
                "widget": "InputField",
                "editable": True,
                "feedback": True
            }
        ]
    })


@pytest.fixture
@pytest.mark.django_db
def item_template_one_input_two_output_one_optional():
    """
    ItemTemplate for item with one input field, and two output fields,
    but one output field is optional (e.g. comment field).
    """
    return ItemTemplate.create_template_from_schema({
        "name": "template",
        "fields": [
            {
                "name": "data_field",
                "widget": "TextLabel"
            },
            {
                "name": "input_field1",
                "widget": "InputField",
                "editable": True,
                "feedback": True
            },
            {
                "name": "input_field2",
                "widget": "InputField",
                "editable": True,
                "feedback": True,
                "required": False
            }
        ]
    })
