from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, SkillViewSet, IndustryViewSet,
    evidence, compare, SavedPlanViewSet, get_courses_by_skills, BookmarkViewSet, DiplomaToDegreeViewSet,
    CareerViewSet, CourseCareerViewSet, CourseIGPViewSet
)

from .auth_views import register, me

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"skills",  SkillViewSet,  basename="skill")
router.register(r"industries", IndustryViewSet, basename="industry")
router.register(r"plans", SavedPlanViewSet, basename="plan")
router.register(r"bookmarks", BookmarkViewSet, basename="bookmark")
router.register(r"pathways", DiplomaToDegreeViewSet, basename="pathways")
router.register(r"careers", CareerViewSet)
router.register(r"career-paths", CourseCareerViewSet)
router.register(r"igp", CourseIGPViewSet, basename="igp")

urlpatterns = [
    path("courses/by-skills/", get_courses_by_skills, name="get_courses_by_skills"),
    path("", include(router.urls)),
    path("evidence/", evidence),
    path("compare/", compare),


    # auth helpers
    path("auth/register/", register),
    path("auth/me/", me),
    path("auth/login/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("auth/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    # path('', include('skillsbridge_sg.urls')),
]

