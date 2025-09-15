from django.urls import path
from .views import upload_metrics_csv, upload_course_skills_csv

urlpatterns = [
    path("datasets/upload/", upload_metrics_csv),
    path("course-skills/upload/", upload_course_skills_csv),
]