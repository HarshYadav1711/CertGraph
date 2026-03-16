"""
Management command to seed sample data for CertGraph APIs.

Usage:
    python manage.py seed_data

This command creates a small but realistic graph of vendors, products,
courses, certifications, and their mappings so reviewers can exercise
the API surface quickly.
"""

from django.core.management.base import BaseCommand

from certification.models import Certification
from course.models import Course
from course_certification_mapping.models import CourseCertificationMapping
from product.models import Product
from product_course_mapping.models import ProductCourseMapping
from vendor.models import Vendor
from vendor_product_mapping.models import VendorProductMapping


class Command(BaseCommand):
    help = "Seed sample vendors, products, courses, certifications, and mappings."

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample data...")

        # Clear existing objects to keep the seed deterministic.
        CourseCertificationMapping.objects.all().delete()
        ProductCourseMapping.objects.all().delete()
        VendorProductMapping.objects.all().delete()
        Certification.objects.all().delete()
        Course.objects.all().delete()
        Product.objects.all().delete()
        Vendor.objects.all().delete()

        # Vendors
        aws = Vendor.objects.create(
            name="Amazon Web Services",
            code="AWS",
            description="Cloud services provider offering compute, storage, and other services.",
        )
        azure = Vendor.objects.create(
            name="Microsoft Azure",
            code="AZURE",
            description="Cloud platform by Microsoft for building, deploying, and managing applications.",
        )

        # Products
        aws_security = Product.objects.create(
            name="AWS Security",
            code="AWS-SEC",
            description="Security and identity services on AWS.",
            vendor=aws,
        )
        aws_data = Product.objects.create(
            name="AWS Data Analytics",
            code="AWS-DATA",
            description="Analytics and big data services on AWS.",
            vendor=aws,
        )
        azure_security = Product.objects.create(
            name="Azure Security",
            code="AZ-SEC",
            description="Security and identity services on Azure.",
            vendor=azure,
        )

        # Courses
        course_aws_sec_foundations = Course.objects.create(
            name="AWS Security Foundations",
            code="COURSE-AWS-SEC-FOUND",
            description="Introduction to core AWS security services and best practices.",
            product=aws_security,
        )
        course_aws_data_analytics = Course.objects.create(
            name="AWS Data Analytics Essentials",
            code="COURSE-AWS-DATA-ESS",
            description="Key AWS services for data ingestion, storage, and analytics.",
            product=aws_data,
        )
        course_azure_sec_foundations = Course.objects.create(
            name="Azure Security Foundations",
            code="COURSE-AZ-SEC-FOUND",
            description="Overview of Azure security services and governance.",
            product=azure_security,
        )

        # Certifications
        cert_aws_security_specialty = Certification.objects.create(
            name="AWS Security Specialty",
            code="CERT-AWS-SEC-SPC",
            description="Certification focused on securing workloads on AWS.",
            course=course_aws_sec_foundations,
        )
        cert_aws_data_analytics_specialty = Certification.objects.create(
            name="AWS Data Analytics Specialty",
            code="CERT-AWS-DATA-SPC",
            description="Certification focused on designing and operating analytics solutions on AWS.",
            course=course_aws_data_analytics,
        )
        cert_azure_security_engineer = Certification.objects.create(
            name="Azure Security Engineer Associate",
            code="CERT-AZ-SEC-ENG",
            description="Certification focused on implementing Azure security controls and threat protection.",
            course=course_azure_sec_foundations,
        )

        # Vendor–Product mappings
        VendorProductMapping.objects.create(
            parent=aws,
            child=aws_security,
            primary_mapping=True,
        )
        VendorProductMapping.objects.create(
            parent=aws,
            child=aws_data,
            primary_mapping=False,
        )
        VendorProductMapping.objects.create(
            parent=azure,
            child=azure_security,
            primary_mapping=True,
        )

        # Product–Course mappings
        ProductCourseMapping.objects.create(
            parent=aws_security,
            child=course_aws_sec_foundations,
            primary_mapping=True,
        )
        ProductCourseMapping.objects.create(
            parent=aws_data,
            child=course_aws_data_analytics,
            primary_mapping=True,
        )
        ProductCourseMapping.objects.create(
            parent=azure_security,
            child=course_azure_sec_foundations,
            primary_mapping=True,
        )

        # Course–Certification mappings
        CourseCertificationMapping.objects.create(
            parent=course_aws_sec_foundations,
            child=cert_aws_security_specialty,
            primary_mapping=True,
        )
        CourseCertificationMapping.objects.create(
            parent=course_aws_data_analytics,
            child=cert_aws_data_analytics_specialty,
            primary_mapping=True,
        )
        CourseCertificationMapping.objects.create(
            parent=course_azure_sec_foundations,
            child=cert_azure_security_engineer,
            primary_mapping=True,
        )

        self.stdout.write(self.style.SUCCESS("Sample data seeded successfully."))

