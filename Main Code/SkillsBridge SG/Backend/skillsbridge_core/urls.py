from django.urls import path
from skillsbridge_core import views

urlpatterns = [
    path("api/courses/", views.get_courses, name="get_courses"),
]
