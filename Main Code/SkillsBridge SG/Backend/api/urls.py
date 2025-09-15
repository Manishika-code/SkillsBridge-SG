from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, SkillViewSet, IndustryViewSet,
    evidence, compare, SavedPlanViewSet
)
from .auth_views import register, me

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"skills",  SkillViewSet,  basename="skill")
router.register(r"industries", IndustryViewSet, basename="industry")
router.register(r"plans", SavedPlanViewSet, basename="plan")

urlpatterns = [
    path("", include(router.urls)),
    path("evidence/", evidence),
    path("compare/", compare),

    # auth helpers
    path("auth/register/", register),
    path("auth/me/", me),
]

