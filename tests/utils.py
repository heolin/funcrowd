from tasks.models import Item, Annotation
from users.models import EndWorker


def add_annotation(item: Item, user: EndWorker, data=None,
                   default_field="output", default_value="1",
                   skipped=False, annotated=True) -> Annotation:
    if not data:
        data = {default_field: default_value}

    annotation, _ = item.get_or_create_annotation(user)
    annotation.data = data
    annotation.annotated = annotated
    annotation.skipped = skipped
    annotation.save()
    annotation.item.update_status()
    user.on_annotation(annotation)
    return annotation
