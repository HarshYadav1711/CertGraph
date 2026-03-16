from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "product", "is_active", "created_at", "updated_at")
    list_filter = ("product", "is_active", "created_at")
    search_fields = ("name", "code", "product__name")
    ordering = ("name",)

