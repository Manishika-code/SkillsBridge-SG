from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch, MagicMock

from skillsbridge_core.models import (
    Skill, Course, CourseSkill, Industry, Metric,
    SavedPlan, SavedPlanNode, Bookmark, CourseIGP,
    DiplomaToDegree, Career, CourseCareer
)
from skillsbridge_core.services import EvidenceService, IndustryService, CompareService
from skillsbridge_core import loaders


# -------------------------------
# MODELS TESTS
# -------------------------------

class SkillAndCourseModelTests(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name="Artificial Intelligence")
        self.course = Course.objects.create(course_name="Computer Science", institution="NTU")

    def test_skill_str(self):
        self.assertEqual(str(self.skill), "Artificial Intelligence")

    def test_course_str(self):
        self.assertIn("Computer Science", str(self.course))
        self.assertIn("NTU", str(self.course))

    def test_course_skill_relation(self):
        rel = CourseSkill.objects.create(course=self.course, skill=self.skill, relevance=0.9)
        self.assertEqual(rel.course, self.course)
        self.assertEqual(rel.skill, self.skill)
        self.assertEqual(rel.relevance, 0.9)


class IndustryMetricTests(TestCase):
    def setUp(self):
        self.industry = Industry.objects.create(name="Information Technology")
        self.course = Course.objects.create(course_name="Data Analytics", institution="NUS")
        self.metric = Metric.objects.create(
            metric_type="employment_rate",
            value=92.5,
            unit="%",
            dataset_vintage=2023,
            source_name="MOE",
            source_url="http://example.com",
            course=self.course,
            industry=self.industry
        )

    def test_metric_saved_correctly(self):
        self.assertEqual(Metric.objects.count(), 1)
        self.assertEqual(self.metric.course.course_name, "Data Analytics")

    def test_metric_value_and_unit(self):
        self.assertEqual(self.metric.unit, "%")
        self.assertEqual(float(self.metric.value), 92.5)

    def test_industry_str(self):
        self.assertEqual(str(self.industry), "Information Technology")


class SavedPlanTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="john")
        self.plan = SavedPlan.objects.create(user=self.user, name="My Plan")
        self.node = SavedPlanNode.objects.create(plan=self.plan, node_type="course", ref_id="123", order_idx=1)

    def test_plan_creation(self):
        self.assertEqual(self.plan.name, "My Plan")
        self.assertEqual(self.plan.user.username, "john")

    def test_plan_nodes_link(self):
        self.assertEqual(self.plan.nodes.count(), 1)
        node = self.plan.nodes.first()
        self.assertEqual(node.node_type, "course")
        self.assertEqual(node.ref_id, "123")


class BookmarkTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="mark")
        self.course = Course.objects.create(course_name="Cybersecurity", institution="SIT")
        self.bookmark = Bookmark.objects.create(user=self.user, course=self.course)

    def test_str(self):
        s = str(self.bookmark)
        self.assertIn("mark", s)
        self.assertIn("Cybersecurity", s)

    def test_unique_together(self):
        with self.assertRaises(Exception):
            Bookmark.objects.create(user=self.user, course=self.course)


class DiplomaToDegreeTests(TestCase):
    def setUp(self):
        self.diploma = Course.objects.create(course_name="Diploma in IT", institution="SP", level="poly")
        self.degree = Course.objects.create(course_name="Bachelor of Computing", institution="NUS", level="uni")
        self.path = DiplomaToDegree.objects.create(diploma=self.diploma, degree=self.degree, relevance_score=0.8)

    def test_str(self):
        s = str(self.path)
        self.assertIn("Diploma in IT", s)
        self.assertIn("Bachelor of Computing", s)

    def test_unique_constraint(self):
        with self.assertRaises(Exception):
            DiplomaToDegree.objects.create(diploma=self.diploma, degree=self.degree)


class CareerAndCourseCareerTests(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name="Data Science")
        self.industry = Industry.objects.create(name="Tech")
        self.course = Course.objects.create(course_name="Computer Engineering", institution="NTU")
        self.career = Career.objects.create(name="Data Analyst", industry=self.industry)
        self.career.skills.add(self.skill)
        self.relation = CourseCareer.objects.create(course=self.course, career=self.career, relevance_score=0.9)

    def test_career_str(self):
        self.assertEqual(str(self.career), "Data Analyst")

    def test_coursecareer_str(self):
        s = str(self.relation)
        self.assertIn("Computer Engineering", s)
        self.assertIn("Data Analyst", s)


# -------------------------------
# SERVICES TESTS
# -------------------------------

class EvidenceServiceTests(TestCase):
    def setUp(self):
        self.industry = Industry.objects.create(name="AI Industry")
        self.course = Course.objects.create(course_name="AI & Robotics", institution="NTU")
        self.metric = Metric.objects.create(
            metric_type="employment_rate",
            value=90,
            unit="%",
            dataset_vintage=2022,
            source_name="MOE",
            source_url="http://example.com",
            course=self.course,
            industry=self.industry
        )

    def test_for_entity_course(self):
        data = EvidenceService.for_entity("course", self.course.id)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["metric_type"], "employment_rate")

    def test_for_entity_industry(self):
        data = EvidenceService.for_entity("industry", self.industry.id)
        self.assertEqual(len(data), 1)

    def test_for_entity_unknown(self):
        data = EvidenceService.for_entity("unknown", "123")
        self.assertEqual(data, [])


class IndustryServiceTests(TestCase):
    def setUp(self):
        self.industry = Industry.objects.create(name="Finance")
        self.metric_new = Metric.objects.create(
            metric_type="employment_rate",
            value=90,
            unit="%",
            dataset_vintage=2024,
            source_name="MAS",
            source_url="http://example.com",
            industry=self.industry
        )
        self.metric_old = Metric.objects.create(
            metric_type="median_salary",
            value=5000,
            unit="$",
            dataset_vintage=2015,
            source_name="Gov",
            source_url="http://example.com",
            industry=self.industry
        )

    def test_context_marks_stale_data(self):
        ctx = IndustryService.context(self.industry.id)
        metrics = ctx["metrics"]
        self.assertTrue(any(m["isStale"] for m in metrics))
        self.assertIn("Finance", ctx["industry"]["name"])


class CompareServiceTests(TestCase):
    def setUp(self):
        self.course1 = Course.objects.create(course_name="AI", institution="NTU")
        self.course2 = Course.objects.create(course_name="Business Analytics", institution="NUS")
        Metric.objects.create(metric_type="employment_rate", value=90, dataset_vintage=2023,
                              source_name="MOE", source_url="x", course=self.course1)
        Metric.objects.create(metric_type="employment_rate", value=95, dataset_vintage=2023,
                              source_name="MOE", source_url="x", course=self.course2)

    def test_compare_courses_returns_expected_structure(self):
        result = CompareService.compare_courses([self.course1.id, self.course2.id])
        self.assertIn("courses", result)
        self.assertIn("metrics", result)
        self.assertEqual(len(result["courses"]), 2)
        self.assertEqual(set(result["metrics"].keys()), {self.course1.id, self.course2.id})


# -------------------------------
# LOADERS TESTS (formatting and cleaning)
# -------------------------------

class LoaderUtilityTests(TestCase):
    def test_format_polytechnic_course(self):
        name = "Cybersecurity & Digital Forensics (Nanyang Polytechnic)"
        formatted = loaders.format_polytechnic_course(name)
        self.assertTrue(formatted.startswith("Diploma in Cybersecurity"))
        self.assertIn("(Nanyang Polytechnic)", formatted)

    def test_format_degree_course(self):
        name = "Mechanical Engineering (Nanyang Technological University)"
        formatted = loaders.format_degree_course(name)
        self.assertTrue(formatted.startswith("Bachelor of"))
        self.assertIn("(Nanyang Technological University)", formatted)

    def test_clean_gpa_value(self):
        self.assertEqual(loaders.clean_gpa_value("364"), "3.64")
        self.assertEqual(loaders.clean_gpa_value("3,85"), "3.85")
        self.assertEqual(loaders.clean_gpa_value("-"), "")

    def test_clean_alevel_value(self):
        self.assertEqual(loaders.clean_alevel_value("aaa/a"), "AAA/A")
        self.assertEqual(loaders.clean_alevel_value("#"), "")

    def test_normalize_name(self):
        result = loaders.normalize_name("Bachelor of Engineering (Hons) in Computer Science")
        self.assertIn("computer science", result)
        self.assertNotIn("bachelor", result)

    def test_extract_placement_from_row(self):
        row = "Aerospace Engineering 181"
        val = loaders.extract_placement_from_row(row)
        self.assertEqual(val, 181)
        self.assertIsNone(loaders.extract_placement_from_row("word only"))

    @patch("skillsbridge_core.loaders.Course.objects")
    def test_find_best_course_match_handles_missing_institution(self, mock_course):
        result = loaders.find_best_course_match("Some Course", None)
        self.assertIsNone(result)

    def test_clean_gpa_invalid_formats(self):
        self.assertEqual(loaders.clean_gpa_value("99"), "")
        self.assertEqual(loaders.clean_gpa_value("text"), "")



