"""
Models for the vendor_product_mapping app.
"""

from django.db import models
from django.db.models import Q

from core.base_models import BaseModel


class VendorProductMapping(BaseModel):
    """
    Represents the relationship between a Vendor (parent) and a Product (child).
    """

    parent = models.ForeignKey(
        "vendor.Vendor",
        on_delete=models.CASCADE,
        related_name="vendor_product_mappings",
    )
    child = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        related_name="product_vendor_mappings",
    )
    primary_mapping = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        db_table = "vendor_product_mapping"
        verbose_name = "Vendor–Product Mapping"
        verbose_name_plural = "Vendor–Product Mappings"
        constraints = [
            # Prevent duplicate parent/child pairs
            models.UniqueConstraint(
                fields=("parent", "child"),
                name="uniq_vendor_product_pair",
            ),
            # Only a single primary mapping per parent
            models.UniqueConstraint(
                fields=("parent",),
                condition=Q(primary_mapping=True),
                name="uniq_primary_vendor_product_per_parent",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.parent} → {self.child}"

