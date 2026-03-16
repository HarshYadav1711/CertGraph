from django.contrib import admin

from .models import ProductCourseMapping


@admin.register(ProductCourseMapping)
class ProductCourseMappingAdmin(admin.ModelAdmin):
    list_display = (
        "parent",
        "child",
        "primary_mapping",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("primary_mapping", "is_active", "created_at")
    search_fields = ("parent__name", "parent__code", "child__name", "child__code")
    ordering = ("parent", "child")

