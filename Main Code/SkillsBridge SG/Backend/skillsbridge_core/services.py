from datetime import datetime
from .models import Course, Industry, Metric 

# this code describes controllers

# returns the data for a specific course or industry
class EvidenceService:
    @staticmethod
    def for_entity(entity: str, id_: str):
        if entity == "course":
            return list(Metric.objects.filter(course_id=id_).values())
        elif entity == "industry":
            return list(Metric.objects.filter(industry_id=id_).values())
        return []

# returns the data for the industry, warn if the data is old
class IndustryService:
    @staticmethod
    def context(industry_id: str):
        ind = Industry.objects.get(pk=industry_id)
        y = datetime.now().year
        metrics = [
            {**m, "isStale": (y - m["dataset_vintage"]) > 3}
            for m in Metric.objects.filter(industry_id=industry_id).values()
        ]
        return {"industry": {"id": ind.id, "name": ind.name}, "metrics": metrics}

# compares one course to another
class CompareService:
    @staticmethod
    def compare_courses(course_ids: list[str]):
        course_ids = course_ids[:2]
        courses = list(Course.objects.filter(id__in=course_ids).values())
        metrics = Metric.objects.filter(course_id__in=course_ids).order_by("metric_type").values()
        grouped = {cid: [] for cid in course_ids}
        for m in metrics:
            grouped[m["course_id"]].append(m)
        return {"courses": courses, "metrics": grouped}