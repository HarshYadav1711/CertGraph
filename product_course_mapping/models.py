"""
Models for the product_course_mapping app.
"""

from django.db import models
from django.db.models import Q

from core.base_models import BaseModel


class ProductCourseMapping(BaseModel):
    """
    Represents the relationship between a Product (parent) and a Course (child).
    """

    parent = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        related_name="product_course_mappings",
    )
    child = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="course_product_mappings",
    )
    primary_mapping = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        db_table = "product_course_mapping"
        verbose_name = "Product–Course Mapping"
        verbose_name_plural = "Product–Course Mappings"
        constraints = [
            models.UniqueConstraint(
                fields=("parent", "child"),
                name="uniq_product_course_pair",
            ),
            models.UniqueConstraint(
                fields=("parent",),
                condition=Q(primary_mapping=True),
                name="uniq_primary_product_course_per_parent",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.parent} → {self.child}"

