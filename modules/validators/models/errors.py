
class AnnotationFormValidationError(object):
    def __init__(self, field, message):
        self.name = self.__class__.__name__
        self.field = field
        self.message = message


class ValueNotInDataSourceError(AnnotationFormValidationError):
    def __init__(self, field):
        super().__init__(field, "Used value was not found in source field.")


class RequiredFieldNotFoundError(AnnotationFormValidationError):
    def __init__(self, field):
        super().__init__(field, "Required field not found in annotation.")


class RequiredFieldEmptyError(AnnotationFormValidationError):
    def __init__(self, field):
        super().__init__(field, "Required field was empty.")


class FieldNotInTemplateError(AnnotationFormValidationError):
    def __init__(self, field):
        super().__init__(field, "Field not found in template")


class FieldTypeError(AnnotationFormValidationError):
    def __init__(self, field, type):
        super().__init__(field, "Type error. Expected type is \"{}\"".format(type))
