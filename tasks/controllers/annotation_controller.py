from tasks.models.dto.annotation_response import AnnotationResponse
from modules.validators.models.annotation import (
    AnnotationFieldsValidator,
    SourceFieldValuesValidator,
    AnnotationDoneValidator
)


class AnnotationController(object):
    validators = [
        AnnotationFieldsValidator(),
        AnnotationDoneValidator(),
        SourceFieldValuesValidator()
    ]

    def process(self, annotation):
        # processing validators
        is_verified, errors = True, []

        if not annotation.skipped:
            for validator in AnnotationController.validators:
                _is_verified, _errors = validator.verify(annotation)
                is_verified = is_verified and _is_verified
                errors.extend(_errors)

        # no error found
        if is_verified:
            # saving annotation
            annotation.save()

            # adding feedback
            task = annotation.item.task
            if hasattr(task, "feedback") and not annotation.skipped:
                task.feedback.create_feedback(annotation)

        response = AnnotationResponse(annotation, is_verified, errors)
        return response

