"""
URL configuration for the vendor app.
"""

from django.urls import path

from .views import VendorDetailAPIView, VendorListCreateAPIView

app_name = "vendor"

urlpatterns = [
    path("vendors/", VendorListCreateAPIView.as_view(), name="vendor-list-create"),
    path("vendors/<int:pk>/", VendorDetailAPIView.as_view(), name="vendor-detail"),
]

