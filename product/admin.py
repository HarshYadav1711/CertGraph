from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "vendor", "is_active", "created_at", "updated_at")
    list_filter = ("vendor", "is_active", "created_at")
    search_fields = ("name", "code", "vendor__name")
    ordering = ("name",)

