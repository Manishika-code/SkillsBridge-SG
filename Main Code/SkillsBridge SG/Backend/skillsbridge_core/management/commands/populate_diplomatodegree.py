
from django.core.management.base import BaseCommand
from django.db.models import Count
from skillsbridge_core.models import Course, DiplomaToDegree

class Command(BaseCommand):
    help = "Auto-generate diploma-to-degree mappings based on shared skills"

    def add_arguments(self, parser):
        parser.add_argument(
            "--threshold",
            type=int,
            default=2,
            help="Minimum number of shared skills required to create a mapping (default: 2)"
        )

    def handle(self, *args, **options):
        threshold = options["threshold"]
        diplomas = Course.objects.filter(level="poly")
        degrees = Course.objects.filter(level="uni")
        created_count = 0

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"Generating mappings with threshold ≥ {threshold}"
        ))

        for diploma in diplomas:
            # Find degrees sharing >= threshold skills
            shared_degrees = (
                degrees.filter(skills__in=diploma.skills.all())
                .annotate(shared=Count("skills"))
                .filter(shared__gte=threshold)
                .distinct()
            )

            for degree in shared_degrees:
                _, created = DiplomaToDegree.objects.get_or_create(
                    diploma=diploma,
                    degree=degree,
                    defaults={"relevance_score": shared_degrees.count()}
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ {created_count} mappings created successfully."
        ))

