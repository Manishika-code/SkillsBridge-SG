import csv, io
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from skillsbridge_core.models import Metric, Course, Skill, CourseSkill

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

@api_view(["POST"])
@permission_classes([IsAdmin])
def upload_metrics_csv(request):
    """
    Upload CSV to insert metrics (UC12).
    CSV headers:
    metric_type,value,unit,dataset_vintage,source_name,source_url,course_id,industry_id
    """
    if "file" not in request.FILES:
        return Response({"error": "csv file required"}, status=400)

    data = request.FILES["file"].read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(data))
    inserted, skipped = 0, 0

    for row in reader:
        try:
            Metric.objects.create(
                metric_type=row["metric_type"],
                value=float(row["value"]),
                unit=row.get("unit") or None,
                dataset_vintage=int(row["dataset_vintage"]),
                source_name=row["source_name"],
                source_url=row["source_url"],
                course_id=row.get("course_id") or None,
                industry_id=row.get("industry_id") or None,
            )
            inserted += 1
        except Exception:
            skipped += 1

    return Response({"inserted": inserted, "skipped": skipped}, status=201)

@api_view(["POST"])
@permission_classes([IsAdmin])
def upload_course_skills_csv(request):
    """
    Upload CSV to link skills with courses (UC12/UC13).
    CSV headers:
    course_id,skill_name,relevance
    """
    if "file" not in request.FILES:
        return Response({"error": "csv file required"}, status=400)

    data = request.FILES["file"].read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(data))
    linked = 0

    for row in reader:
        course = Course.objects.filter(id=row.get("course_id")).first()
        if not course: continue
        skill, _ = Skill.objects.get_or_create(name=row["skill_name"].strip())
        CourseSkill.objects.get_or_create(
            course=course,
            skill=skill,
            defaults={"relevance": float(row.get("relevance") or 1.0)}
        )
        linked += 1

    return Response({"linked": linked}, status=201)