"""
Models for the vendor app.
"""

from django.db import models

from core.base_models import BaseModel


class Vendor(BaseModel):
    """
    Represents a certification vendor.
    """

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        db_table = "vendor"
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

