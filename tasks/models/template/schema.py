"""
Schema that validates input that can be use to read
ItemTemplate and its ItemTemplateFields form a json object.
"""

TEMPLATE_SCHEMA = {
    "type": "object",
    "properties" : {
        "name": {
            "type": "string"
        },
        "fields": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "label": {"type": "string"},
                    "widget": {"type": "string"},
                    "editable":{"type": "boolean"},
                    "required": {"type": "boolean"},
                    "feedback": {"type": "boolean"},
                    "validate_data_source": {"type": "boolean"},
                    "data_source": {"type": "string" }
                },
                "required": ["name", "widget"]
            }
        }
    }
}
