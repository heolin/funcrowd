from .errors import (
    ValueNotInDataSourceError,
    RequiredFieldEmptyError,
    FieldNotInTemplateError,
    RequiredFieldNotFoundError
)

from modules.validators.models.base import FieldValidator


class SourceFieldValuesValidator(FieldValidator):

    def check_errors(self, annotation):
        errors = []
        item = annotation.item
        template = item.template
        for field in template.annotations_fields:
            if field.data_source and field.name in annotation.data:
                if annotation.data[field.name] not in item.data[field.data_source.name]:
                    errors.append(ValueNotInDataSourceError(field.name))
        return errors


class AnnotationFieldsValidator(FieldValidator):

    def check_errors(self, annotation):
        errors = []

        template = annotation.item.template

        data_fields = set(annotation.data.keys())
        for field in template.annotations_fields.all():
            if field.name not in data_fields and field.required:
                errors.append(RequiredFieldNotFoundError(field.name))

        annotations_fields = {field.name for field in template.annotations_fields.all()}
        for field_name in data_fields:
            if field_name not in annotations_fields:
                errors.append(FieldNotInTemplateError(field_name))

        return errors


class AnnotationDoneValidator(FieldValidator):
    def check_errors(self, annotation):
        errors = []

        for field in annotation.item.template.annotations_fields:
            if field.required and field.name in annotation.data:
                if not annotation.data[field.name] and annotation.data[field.name] != 0:
                    errors.append(RequiredFieldEmptyError(field.name))

        return errors
