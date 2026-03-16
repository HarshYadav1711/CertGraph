"""
URL configuration for the vendor_product_mapping app.
"""

from django.urls import path

from .views import (
    VendorProductMappingDetailAPIView,
    VendorProductMappingListCreateAPIView,
)

app_name = "vendor_product_mapping"

urlpatterns = [
    path(
        "vendor-product-mappings/",
        VendorProductMappingListCreateAPIView.as_view(),
        name="vendor-product-mapping-list-create",
    ),
    path(
        "vendor-product-mappings/<int:pk>/",
        VendorProductMappingDetailAPIView.as_view(),
        name="vendor-product-mapping-detail",
    ),
]

