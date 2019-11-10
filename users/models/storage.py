from django.db import models
from django.contrib.postgres.fields import JSONField


class Storage(models.Model):
    key = models.CharField(max_length=100)
    user = models.ForeignKey("EndWorker",
                             on_delete=models.CASCADE,
                             related_name="storages")
    data = JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'key']),
        ]
        unique_together = ('user', 'key')
