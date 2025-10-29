from django.core.management.base import BaseCommand
from skillsbridge_core.models import Skill, Career, Industry

# --- Category → keyword → career list mapping ---
CAREER_LIBRARY = {
    "Infocomm Technology": {
        "keywords": ["code", "software", "cyber", "network", "data", "cloud", "ai", "comput"],
        "roles": [
            # Software / AI / Data
            "Software Engineer", "Backend Developer", "Frontend Developer",
            "Full-Stack Developer", "AI Engineer", "Machine Learning Engineer",
            "Data Scientist", "Data Analyst", "Data Engineer",
            # Cybersecurity
            "Cybersecurity Analyst", "Penetration Tester", "SOC Analyst",
            "Security Engineer", "Incident Responder",
            # Network / Cloud
            "Cloud Engineer", "DevOps Engineer", "Network Engineer",
            "Systems Administrator", "IT Support Specialist",
            "Database Administrator",
        ],
    },
    "Business & Management": {
        "keywords": ["business", "account", "finance", "market", "econ", "manage"],
        "roles": [
            "Business Analyst", "Financial Analyst", "Accountant",
            "Investment Analyst", "Marketing Executive",
            "Operations Manager", "Project Manager",
            "Product Manager", "Entrepreneur", "Human Resource Specialist",
        ],
    },
    "Design & Media": {
        "keywords": ["design", "creative", "graphic", "ui", "ux", "media", "art"],
        "roles": [
            "Graphic Designer", "UX Designer", "UI Designer",
            "Product Designer", "Animator", "3D Artist",
            "Game Designer", "Creative Director",
            "Video Editor", "Visual Effects Artist",
        ],
    },
    "Engineering": {
        "keywords": ["engineer", "mechanic", "electronic", "chemical", "civil", "aero"],
        "roles": [
            "Mechanical Engineer", "Electrical Engineer", "Electronics Engineer",
            "Chemical Engineer", "Civil Engineer", "Industrial Engineer",
            "Systems Engineer", "Aerospace Engineer", "Robotics Engineer",
            "Manufacturing Engineer", "Maintenance Engineer",
        ],
    },
    "Sciences & Healthcare": {
        "keywords": ["bio", "chem", "physic", "health", "nurs", "pharma", "medic"],
        "roles": [
            "Biomedical Scientist", "Chemist", "Physicist",
            "Pharmacist", "Laboratory Technologist",
            "Healthcare Administrator", "Nurse", "Medical Technologist",
            "Public Health Officer", "Clinical Research Associate",
        ],
    },
    "Education & Humanities": {
        "keywords": ["teach", "educ", "psych", "soci", "lang", "hist"],
        "roles": [
            "Teacher", "Lecturer", "Counsellor", "Psychologist",
            "Linguist", "Sociologist", "Historian", "Curriculum Developer",
        ],
    },
    "Built Environment": {
        "keywords": ["build", "arch", "urban", "real", "const"],
        "roles": [
            "Architect", "Urban Planner", "Quantity Surveyor",
            "Real Estate Analyst", "Construction Manager",
            "Landscape Architect", "Facilities Manager",
        ],
    },
}

class Command(BaseCommand):
    help = "Auto-generate a large set of realistic careers based on skills and industries"

    def add_arguments(self, parser):
        parser.add_argument(
            "--link-skills",
            action="store_true",
            help="If provided, attempt to link generated careers to existing Skill objects (case-insensitive match).",
        )

    def handle(self, *args, **options):
        link_skills = options["link_skills"]
        created_count = 0
        linked_count = 0

        for industry_name, data in CAREER_LIBRARY.items():
            industry, _ = Industry.objects.get_or_create(name=industry_name)

            for role in data["roles"]:
                career, created = Career.objects.get_or_create(
                    name=role,
                    defaults={
                        "description": f"Career in {industry_name.lower()} sector.",
                        "industry": industry,
                    },
                )
                if created:
                    created_count += 1

                # Optional: auto-link to skills if flag set
                if link_skills:
                    from django.db import transaction
                    with transaction.atomic():
                        for kw in data["keywords"]:
                            matched_skills = Skill.objects.filter(name__icontains=kw)
                            if matched_skills.exists():
                                career.skills.add(*matched_skills)
                                linked_count += matched_skills.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Created {created_count} careers "
                + (f"and linked {linked_count} skill references." if link_skills else "")
            )
        )

