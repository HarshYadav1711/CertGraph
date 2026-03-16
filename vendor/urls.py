"""
URL configuration for the vendor app.
"""

from django.urls import path

from .views import (
    VendorCertificationPathAPIView,
    VendorDetailAPIView,
    VendorListCreateAPIView,
)

app_name = "vendor"

urlpatterns = [
    path("vendors/", VendorListCreateAPIView.as_view(), name="vendor-list-create"),
    path("vendors/<int:pk>/", VendorDetailAPIView.as_view(), name="vendor-detail"),
    path(
        "vendors/<int:vendor_id>/certification-path/",
        VendorCertificationPathAPIView.as_view(),
        name="vendor-certification-path",
    ),
]

