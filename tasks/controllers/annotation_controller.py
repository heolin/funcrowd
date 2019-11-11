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
        is_verified, exp_base, exp_bonus, errors = True, None, None, []
        user = annotation.user

        if not annotation.skipped:
            for validator in AnnotationController.validators:
                _is_verified, _errors = validator.verify(annotation)
                is_verified = is_verified and _is_verified
                errors.extend(_errors)

        # no error found
        if is_verified:
            # saving annotation
            annotation.annotated = True
            annotation.save()

            # adding feedback
            task = annotation.item.task
            if hasattr(task, "feedback") and not annotation.skipped:
                task.feedback.create_feedback(annotation)

            # update item status
            annotation.item.update_status()
            user.on_annotation(annotation)

            # handle exp
            exp_base, exp_bonus = annotation.get_exp()
            if exp_base:
                user.add_exp(exp_base + exp_bonus)

        response = AnnotationResponse(annotation, is_verified, exp_base, exp_bonus, errors)
        return response

