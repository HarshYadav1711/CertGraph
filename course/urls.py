"""
URL configuration for the course app.
"""

from django.urls import path

from .views import CourseDetailAPIView, CourseListCreateAPIView

app_name = "course"

urlpatterns = [
    path("courses/", CourseListCreateAPIView.as_view(), name="course-list-create"),
    path("courses/<int:pk>/", CourseDetailAPIView.as_view(), name="course-detail"),
]

