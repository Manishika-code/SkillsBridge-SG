from django.core.management.base import BaseCommand
from django.db.models import Count
from skillsbridge_core.models import Course, Career, CourseCareer

class Command(BaseCommand):
    help = "Auto-generate degree-to-career mappings based on shared skills"

    def add_arguments(self, parser):
        parser.add_argument(
            "--threshold",
            type=int,
            default=2,
            help="Minimum shared skills between course and career to create a mapping"
        )

    def handle(self, *args, **options):
        threshold = options["threshold"]
        CourseCareer.objects.all().delete()
        created_count = 0

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"Generating course→career mappings (threshold ≥ {threshold})"
        ))

        # Example heuristic: if a career shares ≥ N skills with a course
        for course in Course.objects.all():
            for career in Career.objects.all():
                shared = course.skills.filter(name__in=[s.name for s in career.skills.all()]).count()
                if shared >= threshold:
                    CourseCareer.objects.get_or_create(
                        course=course,
                        career=career,
                        defaults={"relevance_score": shared}
                    )
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created_count} mappings created."))

