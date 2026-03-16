"""
Serializers for the course_certification_mapping app.
"""

from rest_framework import serializers

from .models import CourseCertificationMapping


class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseCertificationMapping entities.
    """

    class Meta:
        model = CourseCertificationMapping
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
            qs = CourseCertificationMapping.objects.filter(parent=parent, child=child)
            if self.instance is not None:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            "This course is already mapped to the specified certification."
                        ]
                    }
                )

        # Ensure only one primary mapping per parent
        if primary_mapping and parent:
            qs_primary = CourseCertificationMapping.objects.filter(
                parent=parent, primary_mapping=True
            )
            if self.instance is not None:
                qs_primary = qs_primary.exclude(pk=self.instance.pk)
            if qs_primary.exists():
                raise serializers.ValidationError(
                    {
                        "primary_mapping": [
                            "A primary mapping already exists for this course."
                        ]
                    }
                )

        return attrs

