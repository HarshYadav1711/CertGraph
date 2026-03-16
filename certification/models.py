"""
Models for the certification app.
"""

from django.db import models

from core.base_models import BaseModel


class Certification(BaseModel):
    """
    Represents a certification associated with a course.
    """

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="certifications",
    )

    class Meta(BaseModel.Meta):
        db_table = "certification"
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

