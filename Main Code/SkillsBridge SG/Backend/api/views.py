from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.db.models import Sum, Count

from skillsbridge_core.models import Course, Skill, Industry, SavedPlan, CourseSkill, Bookmark, DiplomaToDegree
from .serializers import (
    CourseSerializer, SkillSerializer, IndustrySerializer,
    SavedPlanSerializer, BookmarkSerializer, DiplomaToDegreeSerializer
)
from skillsbridge_core.services import EvidenceService, IndustryService, CompareService

# ---------- Read-only catalog endpoints ----------
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /api/courses/?level=poly&provider=NYP&skills__name=AI
    """
    queryset = Course.objects.all().prefetch_related("skills")
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["level", "provider", "name", "skills__name"]  # needs django-filter

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["name"]

class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["name"]

    @action(detail=True, methods=["get"], url_path="context")
    def context(self, request, pk=None):
        """
        GET /api/industries/<id>/context/
        """
        return Response(IndustryService.context(pk))

# ---------- Supporting endpoints ----------
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def evidence(request):
    """
    GET /api/evidence/?entity=course&id=<uuid>
    GET /api/evidence/?entity=industry&id=<uuid>
    """
    entity = request.query_params.get("entity")
    id_ = request.query_params.get("id")
    if entity not in ("course", "industry") or not id_:
        return Response({"error": "entity∈{course,industry} and id are required"}, status=400)
    return Response(EvidenceService.for_entity(entity, id_))

@api_view(["POST"])
@permission_classes([permissions.AllowAny])  # or tighten if needed
def compare(request):
    """
    POST /api/compare/  body: { "courseIds": ["<idA>","<idB>"] }
    """
    ids = request.data.get("courseIds", [])
    if not isinstance(ids, list) or not 1 <= len(ids) <= 2:
        return Response({"error": "Compare supports 1–2 courses"}, status=400)
    return Response(CompareService.compare_courses(ids))

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_courses_by_skills(request):
    """
    POST /api/courses/by-skills/
    body: { "skills": ["Coding", "Design"], "level": "uni" }

    Returns courses ranked by relevance to selected skills.
    """
    skill_names = request.data.get("skills", [])
    level = request.data.get("level")
    provider = request.data.get("provider")

    if not skill_names:
        return Response({"error": "No skills provided"}, status=status.HTTP_400_BAD_REQUEST)

    skills = Skill.objects.filter(name__in=skill_names)
    if not skills.exists():
        return Response({"matches": []})

    # Apply level and provider filters BEFORE annotate/distinct
    queryset = Course.objects.filter(courseskill__skill__in=skills)

    if level:
        queryset = queryset.filter(level=level)
    if provider:
        queryset = queryset.filter(institution__icontains=provider)

    queryset = (
        queryset.annotate(
            matched_skills=Count("courseskill__skill", distinct=True),
            total_relevance=Sum("courseskill__relevance"),
        )
        .order_by("-matched_skills", "-total_relevance")
        .distinct()
    )

    serializer = CourseSerializer(queryset, many=True)
    return Response(serializer.data)
# ---------- Plans (auth required for writes) ----------
class SavedPlanViewSet(viewsets.ModelViewSet):

    serializer_class = SavedPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedPlan.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --------- Bookmark --------- 
class BookmarkViewSet(viewsets.ViewSet):
    """
        GET /api/bookmarks/ lists all bookmarks
        POST /api/bookmarks/ add bookmark 
        DELETE /api/bookmarks/<course_id> remove bookmarks
    """
    # ensures user is authenticated for bookmark
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """GET /api/bookmarks"""
        bookmarks = Bookmark.objects.filter(user=request.user).select_related("course")
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)

    def create(self, request):
        """POST /api/bookmarks/ body: { "course_id": <id> }"""
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        bookmark, created = Bookmark.objects.get_or_create(user=request.user, course=course)
        if not created:
            return Response({"message": "Course already bookmarked"}, status=status.HTTP_200_OK)

        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, pk=None):
        """DELETE /api/bookmarks/<course_id>/"""
        bookmark = Bookmark.objects.filter(user=request.user, course_id=pk)
        if not bookmark.exists():
            return Response({"error": "Bookmark not found"}, status=status.HTTP_404_NOT_FOUND)

        bookmark.delete()
        return Response({"message": "Bookmark removed"}, status=status.HTTP_204_NO_CONTENT)

class DiplomaToDegreeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /api/pathways/?diploma=<id>   -> get degree options for that diploma
    /api/pathways/?degree=<id>    -> get diplomas that lead to this degree
    """
    queryset = DiplomaToDegree.objects.select_related("diploma", "degree")
    serializer_class = DiplomaToDegreeSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        diploma_id = self.request.query_params.get("diploma")
        degree_id = self.request.query_params.get("degree")

        if diploma_id:
            queryset = queryset.filter(diploma_id=diploma_id)
        if degree_id:
            queryset = queryset.filter(degree_id=degree_id)

        return queryset

