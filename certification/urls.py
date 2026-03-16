"""
URL configuration for the certification app.
"""

from django.urls import path

from .views import CertificationDetailAPIView, CertificationListCreateAPIView

app_name = "certification"

urlpatterns = [
    path(
        "certifications/",
        CertificationListCreateAPIView.as_view(),
        name="certification-list-create",
    ),
    path(
        "certifications/<int:pk>/",
        CertificationDetailAPIView.as_view(),
        name="certification-detail",
    ),
]

