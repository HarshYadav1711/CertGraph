"""
URL configuration for the product_course_mapping app.
"""

from django.urls import path

from .views import (
    ProductCourseMappingDetailAPIView,
    ProductCourseMappingListCreateAPIView,
)

app_name = "product_course_mapping"

urlpatterns = [
    path(
        "product-course-mappings/",
        ProductCourseMappingListCreateAPIView.as_view(),
        name="product-course-mapping-list-create",
    ),
    path(
        "product-course-mappings/<int:pk>/",
        ProductCourseMappingDetailAPIView.as_view(),
        name="product-course-mapping-detail",
    ),
]

