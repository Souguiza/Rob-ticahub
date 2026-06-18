import uuid

from django.conf import settings
from django.db import models


class TimestampedModel(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_%(class)ss",
    )
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True
