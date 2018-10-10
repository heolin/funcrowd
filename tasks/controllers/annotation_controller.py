from tasks.models.dto.annotation_response import AnnotationResponse


class AnnotationController(object):

    def process(self, annotation):
        is_verified = annotation.verify_fields()
        if is_verified:
            annotation.verify_done()
            annotation.save()

        response = AnnotationResponse(annotation, is_verified)
        return response
