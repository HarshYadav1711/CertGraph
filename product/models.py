"""
Models for the product app.
"""

from django.db import models

from core.base_models import BaseModel


class Product(BaseModel):
    """
    Represents a product offered by a vendor.
    """

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    vendor = models.ForeignKey(
        "vendor.Vendor",
        on_delete=models.CASCADE,
        related_name="products",
    )

    class Meta(BaseModel.Meta):
        db_table = "product"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

