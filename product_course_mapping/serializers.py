"""
Serializers for the product_course_mapping app.
"""

from rest_framework import serializers

from .models import ProductCourseMapping


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductCourseMapping entities.
    """

    class Meta:
        model = ProductCourseMapping
        fields = [
            "id",
            "parent",
            "child",
            "primary_mapping",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        parent = attrs.get("parent", getattr(self.instance, "parent", None))
        child = attrs.get("child", getattr(self.instance, "child", None))
        primary_mapping = attrs.get(
            "primary_mapping", getattr(self.instance, "primary_mapping", False)
        )

        # Prevent duplicate parent/child mapping
        if parent and child:
            qs = ProductCourseMapping.objects.filter(parent=parent, child=child)
            if self.instance is not None:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            "This product is already mapped to the specified course."
                        ]
                    }
                )

        # Ensure only one primary mapping per parent
        if primary_mapping and parent:
            qs_primary = ProductCourseMapping.objects.filter(
                parent=parent, primary_mapping=True
            )
            if self.instance is not None:
                qs_primary = qs_primary.exclude(pk=self.instance.pk)
            if qs_primary.exists():
                raise serializers.ValidationError(
                    {
                        "primary_mapping": [
                            "A primary mapping already exists for this product."
                        ]
                    }
                )

        return attrs

