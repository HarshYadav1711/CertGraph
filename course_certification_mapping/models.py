"""
Models for the course_certification_mapping app.
"""

from django.db import models
from django.db.models import Q

from core.base_models import BaseModel


class CourseCertificationMapping(BaseModel):
    """
    Represents the relationship between a Course (parent) and a Certification
    (child).
    """

    parent = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="course_certification_mappings",
    )
    child = models.ForeignKey(
        "certification.Certification",
        on_delete=models.CASCADE,
        related_name="certification_course_mappings",
    )
    primary_mapping = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        db_table = "course_certification_mapping"
        verbose_name = "Course–Certification Mapping"
        verbose_name_plural = "Course–Certification Mappings"
        constraints = [
            models.UniqueConstraint(
                fields=("parent", "child"),
                name="uniq_course_certification_pair",
            ),
            models.UniqueConstraint(
                fields=("parent",),
                condition=Q(primary_mapping=True),
                name="uniq_primary_course_certification_per_parent",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.parent} → {self.child}"

