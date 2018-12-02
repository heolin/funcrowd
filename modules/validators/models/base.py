

class FieldValidator(object):

    def check_errors(self, annotation):
        return []

    def verify(self, annotation):
        errors = self.check_errors(annotation)
        is_verified = len(errors) == 0
        return is_verified, errors

