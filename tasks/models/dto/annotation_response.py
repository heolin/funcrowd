
class AnnotationResponse(object):
    def __init__(self, annotation, is_verified, exp_base, exp_bonus, errors):
        self.annotation = annotation
        self.is_verified = is_verified
        self.errors = errors
        self.exp_base = exp_base
        self.exp_bonus = exp_bonus
