from django.core.management.base import BaseCommand
from skillsbridge_core.models import Course, Skill, CourseSkill
import re


class Command(BaseCommand):
    help = "Populate CourseSkill relationships with relevance scoring and robust fallbacks for missing descriptions."

    def handle(self, *args, **options):

        # ===============================================================
        # 1. SKILL DEFINITIONS
        # ===============================================================
        skill_map = {
            # --- TECHNOLOGY & COMPUTING ---
            "Coding": [
                "programming", "software", "developer", "code", "python", "java", "c++", "web", "database",
                "algorithm", "machine learning", "artificial intelligence", "ai", "data", "cloud",
                "cybersecurity", "network", "backend", "frontend", "computing", "information technology",
                "it", "app", "mobile"
            ],
            "Cybersecurity": [
                "security", "cybersecurity", "hacking", "penetration testing", "network security",
                "digital forensics", "malware", "encryption", "cryptography", "ethical hacking"
            ],
            "Data Science": [
                "data", "analytics", "data science", "statistics", "visualization", "machine learning",
                "predictive", "ai", "big data", "modelling", "analysis", "business intelligence"
            ],
            "Artificial Intelligence": [
                "ai", "machine learning", "neural network", "deep learning", "nlp", "artificial intelligence",
                "robotics", "automation", "computer vision"
            ],
            "Networking": [
                "network", "infrastructure", "systems", "server", "cloud", "networking", "iot",
                "wireless", "communication system", "routing", "switching"
            ],
            "Electronics": [
                "electrical", "electronic", "circuit", "semiconductor", "hardware", "signal",
                "embedded", "microcontroller", "robotics", "power", "communication system"
            ],
            "Engineering Design": [
                "mechanical", "engineering", "design", "manufacturing", "automation", "mechatronic",
                "aerospace", "thermodynamics", "materials", "energy", "process", "industrial", "chemical"
            ],
            "Information Systems": [
                "information system", "enterprise", "database", "business analytics", "systems analysis",
                "digital transformation", "erp", "crm", "cloud"
            ],

            # --- BUSINESS, FINANCE & MANAGEMENT ---
            "Business Management": [
                "business", "management", "operations", "organization", "strategy", "leadership",
                "entrepreneurship", "startup", "project management"
            ],
            "Marketing": [
                "marketing", "advertising", "branding", "digital marketing", "social media", "consumer", "campaign"
            ],
            "Finance": [
                "finance", "investment", "accounting", "economics", "banking", "financial", "market",
                "valuation", "policy"
            ],
            "Human Resources": [
                "human resource", "recruitment", "organizational behavior", "talent", "employment law",
                "training", "hr"
            ],
            "Entrepreneurship": [
                "entrepreneurship", "startup", "innovation", "venture", "business creation", "product launch"
            ],
            "Economics": [
                "economics", "market", "microeconomics", "macroeconomics", "trade", "policy", "finance"
            ],

            # --- DESIGN, MEDIA & ARTS ---
            "Design": [
                "design", "creative", "product design", "interface", "ux", "ui", "industrial design",
                "human-centred design"
            ],
            "Graphic Design": [
                "graphic", "illustration", "visual", "typography", "photoshop", "adobe", "animation", "branding"
            ],
            "Architecture": [
                "architecture", "urban planning", "interior design", "landscape", "built environment"
            ],
            "Media & Communication": [
                "communication", "media", "mass communication", "journalism", "broadcast", "advertising",
                "film", "tv"
            ],
            "Performing Arts": [
                "music", "theatre", "drama", "dance", "performance", "acting", "stage"
            ],
            "Fine Arts": [
                "art", "fine art", "painting", "sculpture", "photography", "studio art"
            ],
            "Game Design": [
                "game", "gaming", "interactive media", "simulation", "game development", "unity", "unreal"
            ],
            "Fashion Design": [
                "fashion", "textile", "clothing", "style", "apparel", "merchandising"
            ],

            # --- SCIENCE, MATH & ENVIRONMENT ---
            "Science": [
                "science", "biology", "chemistry", "physics", "laboratory", "experiment", "research", "biomedical"
            ],
            "Mathematics": [
                "math", "algebra", "calculus", "geometry", "statistics", "probability", "quantitative", "numerical"
            ],
            "Environmental Science": [
                "environment", "sustainability", "climate", "ecology", "geography", "marine", "ocean", "earth", "water"
            ],
            "Chemistry": [
                "chemical", "chemistry", "compound", "reaction", "organic", "laboratory"
            ],
            "Biology": [
                "biology", "biological", "life science", "genetics", "microbiology", "biotechnology", "cell"
            ],
            "Physics": [
                "physics", "mechanics", "energy", "quantum", "optics", "dynamics", "waves"
            ],
            "Food Science": [
                "food", "nutrition", "biochemistry", "diet", "health science"
            ],

            # --- HEALTHCARE & SOCIAL SCIENCES ---
            "Nursing": [
                "nursing", "clinical", "hospital", "patient", "care", "healthcare", "medicine", "pharmacy"
            ],
            "Psychology": [
                "psychology", "cognitive", "behavioral", "mental health", "therapy", "neuroscience"
            ],
            "Social Work": [
                "social work", "community", "welfare", "youth", "elderly", "counselling", "non-profit"
            ],
            "Education": [
                "education", "teaching", "pedagogy", "curriculum", "child", "learning", "training"
            ],
            "Public Health": [
                "public health", "epidemiology", "disease", "population", "health policy"
            ],
            "Medicine": [
                "medical", "doctor", "anatomy", "surgery", "pharmacology", "pathology"
            ],

            # --- HUMANITIES, LAW & PUBLIC SERVICE ---
            "Law": [
                "law", "legal", "justice", "crime", "legislation", "policy", "contract", "ethics"
            ],
            "Political Science": [
                "political", "government", "policy", "international relations", "public administration"
            ],
            "History": [
                "history", "historical", "civilization", "heritage", "archaeology"
            ],
            "Philosophy": [
                "philosophy", "ethics", "logic", "critical thinking"
            ],
            "Linguistics": [
                "language", "linguistics", "translation", "english", "communication"
            ],

            # --- CROSS-DISCIPLINARY / SOFT SKILLS ---
            "Public Speaking": [
                "communication", "presentation", "speech", "leadership", "debate", "negotiation", "persuasion"
            ],
            "Creative Writing": [
                "writing", "story", "creative writing", "literature", "poetry", "narrative", "english"
            ],
            "Project Management": [
                "project", "planning", "timeline", "agile", "scrum", "operations", "delivery"
            ],
            "Innovation": [
                "innovation", "creative", "design thinking", "prototype", "invention"
            ],
            "Sustainability": [
                "sustainability", "green", "renewable", "climate", "environmental"
            ]
        }

        # ===============================================================
        # 2. FALLBACK KEYWORDS
        # ===============================================================
        name_fallbacks = {
            "Coding": ["computing", "information technology", "informatics", "software", "data", "it"],
            "Cybersecurity": ["security", "cyber"],
            "Design": ["design", "creative", "interface", "architecture"],
            "Engineering Design": ["engineering", "mechanical", "electrical"],
            "Business Management": ["business", "management", "commerce"],
            "Finance": ["finance", "accounting", "banking", "investment"],
            "Economics": ["economics", "policy", "trade"],
            "Science": ["science", "biomedical", "life science"],
            "Mathematics": ["math", "analytics", "statistics"],
            "Nursing": ["nursing", "healthcare", "medical"],
            "Education": ["education", "teaching", "training"],
            "Architecture": ["architecture", "built environment"],
            "Media & Communication": ["communication", "media", "journalism"],
            "Law": ["law", "legal", "justice"],
            "Political Science": ["policy", "public administration", "international relations"],
            "Data Science": ["data", "analytics", "statistics"],
            "Artificial Intelligence": ["ai", "machine learning"],
            "Innovation": ["innovation", "prototype", "design thinking"],
            "Psychology": ["psychology", "mental", "behavioral"],
            "Medicine": ["medical", "doctor"],
            "Public Health": ["health", "public"],
            "Environmental Science": ["environment", "sustainability"],
            "Project Management": ["project", "planning", "management"],
        }

        school_fallbacks = {
            "School of Computing": "Coding",
            "School of Information Systems": "Information Systems",
            "School of Design": "Design",
            "School of Engineering": "Engineering Design",
            "School of Business": "Business Management",
            "School of Accountancy": "Finance",
            "School of Humanities": "Creative Writing",
            "School of Law": "Law",
            "School of Social Sciences": "Psychology",
            "School of Applied Science": "Science",
            "School of Health": "Nursing",
            "School of Media": "Media & Communication",
            "School of Architecture": "Architecture"
        }

        # ===============================================================
        # 3. ENSURE SKILLS EXIST IN DB
        # ===============================================================
        for name in skill_map.keys():
            Skill.objects.get_or_create(name=name)

        skills = {s.name: s for s in Skill.objects.all()}

        missing = set(skill_map.keys()) - set(skills.keys())
        if missing:
            self.stdout.write(self.style.WARNING(f"⚠️ Missing skills: {', '.join(missing)}"))
            return

        # ===============================================================
        # 4. MATCH COURSES
        # ===============================================================
        total_links = 0
        for course in Course.objects.all():
            desc = (course.course_description or "").lower()
            name = (course.course_name or "").lower()
            school = (course.school or "").lower()
            institution = (course.institution or "").lower()
            linked = False

            for skill_name, keywords in skill_map.items():
                count = sum(len(re.findall(r"\b" + re.escape(k) + r"\b", desc)) for k in keywords)

                # --- Fallback: check course name keywords safely
                if count == 0:
                    fallback_keywords = name_fallbacks.get(skill_name, [])
                    count = sum(len(re.findall(r"\b" + re.escape(k) + r"\b", name)) for k in fallback_keywords)

                # --- Fallback: check school/institution name
                if count == 0:
                    for school_name, fallback_skill in school_fallbacks.items():
                        if fallback_skill == skill_name and school_name.lower() in school + institution:
                            count = 1
                            break

                if count > 0:
                    relevance = min(1.0 + 0.3 * count, 3.0)
                    CourseSkill.objects.update_or_create(
                        course=course,
                        skill=skills[skill_name],
                        defaults={'relevance': relevance}
                    )
                    total_links += 1
                    linked = True

            # Optional generic fallback
            if not linked and "engineering" in name:
                CourseSkill.objects.get_or_create(
                    course=course,
                    skill=skills["Electronics"],
                    defaults={'relevance': 1.2}
                )
                total_links += 1

        # ===============================================================
        # 5. DONE
        # ===============================================================
        self.stdout.write(self.style.SUCCESS(f"✅ Linked {total_links} CourseSkill relationships successfully!"))

