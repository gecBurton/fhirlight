import uuid

from django.db import models
from polymorphic.models import PolymorphicModel


class BaseProfile(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.CharField(
        primary_key=True,
        editable=False,
        unique=True,
        max_length=256,
        default=uuid.uuid4,
    )
    active = models.BooleanField(
        default=True, help_text="Whether the record is still in active use"
    )

    class Meta:
        ordering = ("-created_at",)
