"""
Models for the course app.
"""

from django.db import models

from core.base_models import BaseModel


class Course(BaseModel):
    """
    Represents a course associated with a product.
    """

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        related_name="courses",
    )

    class Meta(BaseModel.Meta):
        db_table = "course"
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

