from tasks.models import Item, Annotation
from users.models import EndWorker


def add_annotation(item: Item, user: EndWorker, data=None,
                   field_name="input_field", value="1",
                   skipped=False, annotated=True) -> Annotation:
    if not data:
        data = { field_name: value }

    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = data
    annotation.annotated = annotated
    annotation.skipped = skipped
    annotation.save()
    annotation.item.update_status()
    user.on_annotation(annotation)
    return annotation
