"""
Reusable abstract base models for the certgraph project.

These models provide common fields for soft delete support and automatic
timestamping. All future concrete models should inherit from
``BaseModel`` to ensure consistency across the domain.
"""

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model providing common audit fields.

    - ``is_active``: boolean flag for soft-delete semantics.
    - ``created_at``: automatically set when the object is first created.
    - ``updated_at``: automatically updated on each save.
    """

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

