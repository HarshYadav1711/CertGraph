"""
Service layer for building certification paths and related domain logic.
"""

from typing import Any, Dict, List

from certification.models import Certification
from core.utils.object_helpers import get_object_or_404_custom
from course.models import Course
from course_certification_mapping.models import CourseCertificationMapping
from product.models import Product
from product_course_mapping.models import ProductCourseMapping
from vendor.models import Vendor
from vendor_product_mapping.models import VendorProductMapping
from vendor.serializers import VendorSerializer


def get_vendor_certification_path(vendor_id: int) -> Dict[str, Any]:
    """
    Build the full certification path for a vendor.

    Structure:
    {
      "vendor": <VendorSerializer data>,
      "products": [
        {
          "product": {...},
          "courses": [
            {
              "course": {...},
              "certifications": [{...}, ...]
            }
          ]
        }
      ]
    }
    """
    vendor = get_object_or_404_custom(Vendor, pk=vendor_id)

    # Products linked via VendorProductMapping
    product_mappings = VendorProductMapping.objects.filter(parent=vendor).select_related(
        "child"
    )
    products: List[Product] = [mapping.child for mapping in product_mappings]
    product_ids = [p.id for p in products]

    if not product_ids:
        return {"vendor": VendorSerializer(vendor).data, "products": []}

    # Courses linked via ProductCourseMapping
    product_course_mappings = ProductCourseMapping.objects.filter(
        parent_id__in=product_ids
    ).select_related("child")
    courses: List[Course] = [m.child for m in product_course_mappings]
    course_ids = [c.id for c in courses]

    # Certifications linked via CourseCertificationMapping
    course_cert_mappings: List[
        CourseCertificationMapping
    ] = CourseCertificationMapping.objects.filter(parent_id__in=course_ids).select_related(
        "child"
    )

    # Index courses and certifications by their parents for efficient nesting
    courses_by_product: Dict[int, List[Course]] = {}
    for mapping in product_course_mappings:
        courses_by_product.setdefault(mapping.parent_id, []).append(mapping.child)

    certs_by_course: Dict[int, List[Certification]] = {}
    for mapping in course_cert_mappings:
        certs_by_course.setdefault(mapping.parent_id, []).append(mapping.child)

    vendor_data = VendorSerializer(vendor).data

    products_payload: List[Dict[str, Any]] = []
    for product in products:
        product_payload: Dict[str, Any] = {
            "product": {
                "id": product.id,
                "name": product.name,
                "code": product.code,
                "description": product.description,
                "is_active": product.is_active,
            },
            "courses": [],
        }

        product_courses = courses_by_product.get(product.id, [])
        for course in product_courses:
            course_payload: Dict[str, Any] = {
                "course": {
                    "id": course.id,
                    "name": course.name,
                    "code": course.code,
                    "description": course.description,
                    "is_active": course.is_active,
                },
                "certifications": [],
            }

            course_certs = certs_by_course.get(course.id, [])
            course_payload["certifications"] = [
                {
                    "id": cert.id,
                    "name": cert.name,
                    "code": cert.code,
                    "description": cert.description,
                    "is_active": cert.is_active,
                }
                for cert in course_certs
            ]

            product_payload["courses"].append(course_payload)

        products_payload.append(product_payload)

    return {
        "vendor": vendor_data,
        "products": products_payload,
    }

