"""
URL configuration for the course_certification_mapping app.
"""

from django.urls import path

from .views import (
    CourseCertificationMappingDetailAPIView,
    CourseCertificationMappingListCreateAPIView,
)

app_name = "course_certification_mapping"

urlpatterns = [
    path(
        "course-certification-mappings/",
        CourseCertificationMappingListCreateAPIView.as_view(),
        name="course-certification-mapping-list-create",
    ),
    path(
        "course-certification-mappings/<int:pk>/",
        CourseCertificationMappingDetailAPIView.as_view(),
        name="course-certification-mapping-detail",
    ),
]

