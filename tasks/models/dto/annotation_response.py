
class AnnotationResponse(object):
    def __init__(self, annotation, is_verified, exp, errors):
        self.annotation = annotation
        self.is_verified = is_verified
        self.errors = errors
        self.exp = exp
