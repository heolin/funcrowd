from .errors import (
    FieldTypeError
)

from modules.validators.models.base import FieldValidator


class FieldTypeValidator(FieldValidator):

    def check_errors(self, annotation):
        errors = []
        item = annotation.item
        template = item.template
        for field in template.annotations_fields:
            if field.name in annotation.data:
                value = annotation.data[field.name]
                if field.type != type(value).__name__ and value:
                    errors.append(FieldTypeError(field.name, field.type))
        return errors
