"""
Root URL configuration for the certgraph project.

This module wires up:

- Django admin at ``/admin/``
- OpenAPI schema in JSON/YAML format
- Swagger UI at ``/swagger/``
- ReDoc UI at ``/redoc/``
"""

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="CertGraph API",
        default_version="v1",
        description="API documentation for the CertGraph backend.",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Documentation
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    # API entrypoints
    path("api/", include("vendor.urls")),
    path("api/", include("product.urls")),
    path("api/", include("course.urls")),
    path("api/", include("certification.urls")),
    path("api/", include("vendor_product_mapping.urls")),
    path("api/", include("product_course_mapping.urls")),
    path("api/", include("course_certification_mapping.urls")),
]
