from django.contrib import admin

from .models import Certification


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "course", "is_active", "created_at", "updated_at")
    list_filter = ("course", "is_active", "created_at")
    search_fields = ("name", "code", "course__name")
    ordering = ("name",)

