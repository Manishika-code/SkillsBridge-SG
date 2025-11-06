from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch

from skillsbridge_core.models import (
    Skill, Course, Industry, Bookmark, DiplomaToDegree,
    Career, CourseCareer, CourseIGP, Metric
)


# -------------------------------
# SERIALIZER TESTS
# -------------------------------

from api.serializers import (
    SkillSerializer, CourseSerializer, IndustrySerializer,
    BookmarkSerializer, DiplomaToDegreeSerializer,
    CareerSerializer, CourseCareerSerializer, CourseIGPSerializer
)


class SerializerTests(APITestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name="Cybersecurity")
        self.course = Course.objects.create(course_name="Information Security", institution="NUS")
        self.course.skills.add(self.skill)
        self.industry = Industry.objects.create(name="IT Industry")
        self.career = Career.objects.create(name="Penetration Tester", industry=self.industry)

    def test_skill_serializer(self):
        data = SkillSerializer(self.skill).data
        self.assertEqual(data["name"], "Cybersecurity")

    def test_course_serializer_includes_skills(self):
        data = CourseSerializer(self.course).data
        self.assertIn("skills", data)
        self.assertEqual(data["skills"][0]["name"], "Cybersecurity")

    def test_industry_serializer(self):
        data = IndustrySerializer(self.industry).data
        self.assertEqual(data["name"], "IT Industry")

    def test_career_serializer(self):
        data = CareerSerializer(self.career).data
        self.assertEqual(data["name"], "Penetration Tester")


# -------------------------------
# AUTHENTICATION TESTS
# -------------------------------

from api.auth_views import RegisterSerializer


class AuthViewsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/auth/register/"

    def test_register_user_successfully(self):
        data = {"username": "newuser", "email": "x@x.com", "password": "securepass123", "role": "student"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_user_validation_error(self):
        response = self.client.post(self.register_url, {"username": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", str(response.content))

    def test_me_requires_auth(self):
        url = "/api/auth/me/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)


# -------------------------------
# COURSE + SKILL API TESTS
# -------------------------------

class CourseSkillEndpointTests(APITestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name="AI")
        self.course = Course.objects.create(course_name="Computer Science", institution="NTU")
        self.course.skills.add(self.skill)

    def test_get_courses_by_skills(self):
        url = "/api/courses/by-skills/"
        data = {"skills": ["AI"]}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("Computer Science" in c["course_name"] for c in response.data))

    def test_get_courses_by_skills_no_skills(self):
        url = "/api/courses/by-skills/"
        response = self.client.post(url, {"skills": []}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_get_courses_by_skills_invalid_name(self):
        url = "/api/courses/by-skills/"
        response = self.client.post(url, {"skills": ["NonexistentSkill"]}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["matches"] if "matches" in response.data else [], [])


# -------------------------------
# EVIDENCE + COMPARE ENDPOINTS
# -------------------------------

class EvidenceCompareTests(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(course_name="Computer Engineering", institution="NUS")
        self.industry = Industry.objects.create(name="Tech")
        Metric.objects.create(metric_type="employment_rate", value=90, unit="%", dataset_vintage=2024,
                              source_name="MOE", source_url="x", course=self.course)
        Metric.objects.create(metric_type="median_salary", value=5000, unit="$", dataset_vintage=2023,
                              source_name="MOE", source_url="x", industry=self.industry)

    def test_evidence_for_course(self):
        url = "/api/evidence/"
        response = self.client.get(url, {"entity": "course", "id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_evidence_invalid_request(self):
        url = "/api/evidence/"
        response = self.client.get(url, {"entity": "invalid"})
        self.assertEqual(response.status_code, 400)

    @patch("api.views.CompareService.compare_courses")
    def test_compare_endpoint(self, mock_compare):
        mock_compare.return_value = {"courses": [], "metrics": {}}
        url = "/api/compare/"
        data = {"courseIds": [str(self.course.id)]}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("courses", response.data)

    def test_compare_invalid_ids(self):
        url = "/api/compare/"
        response = self.client.post(url, {"courseIds": []}, format="json")
        self.assertEqual(response.status_code, 400)


# -------------------------------
# INDUSTRY CONTEXT TEST
# -------------------------------

class IndustryContextTests(APITestCase):
    def setUp(self):
        self.industry = Industry.objects.create(name="Finance")
        Metric.objects.create(metric_type="employment_rate", value=85, unit="%", dataset_vintage=2020,
                              source_name="Gov", source_url="x", industry=self.industry)
        self.url = f"/api/industries/{self.industry.id}/context/"

    def test_industry_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("metrics", response.data)
        self.assertIn("industry", response.data)


# -------------------------------
# BOOKMARK ENDPOINT TESTS
# -------------------------------

class BookmarkViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.client.login(username="tester", password="12345")
        self.course = Course.objects.create(course_name="InfoSec", institution="NYP")
        self.url = "/api/bookmarks/"

    def test_add_bookmark(self):
        response = self.client.post(self.url, {"course_id": self.course.id}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["course"]["course_name"], "InfoSec")

    def test_add_bookmark_missing_course(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_list_bookmarks(self):
        Bookmark.objects.create(user=self.user, course=self.course)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data, list))

    def test_remove_bookmark(self):
        bm = Bookmark.objects.create(user=self.user, course=self.course)
        response = self.client.delete(f"/api/bookmarks/{self.course.id}/")
        self.assertEqual(response.status_code, 204)

    def test_remove_nonexistent_bookmark(self):
        response = self.client.delete(f"/api/bookmarks/999/")
        self.assertEqual(response.status_code, 404)


# -------------------------------
# DIPLOMA TO DEGREE + CAREER TESTS
# -------------------------------

class DiplomaCareerViewTests(APITestCase):
    def setUp(self):
        self.diploma = Course.objects.create(course_name="Diploma in AI", institution="SP", level="poly")
        self.degree = Course.objects.create(course_name="Bachelor of Computing", institution="NUS", level="uni")
        self.pathway = DiplomaToDegree.objects.create(diploma=self.diploma, degree=self.degree, relevance_score=1.0)
        self.industry = Industry.objects.create(name="IT")
        self.career = Career.objects.create(name="AI Engineer", industry=self.industry)
        self.cc = CourseCareer.objects.create(course=self.degree, career=self.career, relevance_score=0.9)

    def test_diploma_to_degree_list(self):
        url = "/api/pathways/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("diploma", response.data[0])

    def test_filter_pathways_by_diploma(self):
        url = f"/api/pathways/?diploma={self.diploma.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("Diploma" in c["diploma"]["course_name"] for c in response.data))

    def test_career_paths_endpoint(self):
        url = f"/api/career-paths/?course={self.degree.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("AI Engineer" in r["career"]["name"] for r in response.data))


# -------------------------------
# COURSE IGP ENDPOINT
# -------------------------------

class CourseIGPViewTests(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(course_name="Business Analytics", institution="SMU")
        CourseIGP.objects.create(
            course=self.course, qualification="poly",
            indicative_grade="3.80", grade_type="GPA", source_url="http://example.com"
        )
        self.url = "/api/igp/"

    def test_list_igp_entries(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("indicative_grade", response.data[0])

    def test_filter_by_course(self):
        response = self.client.get(f"{self.url}?course__id={self.course.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["course"], self.course.id)

