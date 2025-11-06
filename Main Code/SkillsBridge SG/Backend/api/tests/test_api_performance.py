import time
from django.test import TestCase
from django.contrib.auth.models import User
from django.db import connection
from skillsbridge_core.models import Skill, Course, CourseSkill, Industry, Bookmark


class QueryCountMixin:
    """Utility mixin to measure executed queries."""
    def assertNumQueriesLessThan(self, max_queries):
        """Assert that the number of queries stays below threshold."""
        num_queries = len(connection.queries)
        self.assertLessEqual(
            num_queries, max_queries,
            msg=f"Expected <= {max_queries} queries but got {num_queries}"
        )


# ------------------------------------------
# /api/courses/by-skills/
# ------------------------------------------
class CourseSkillPerformanceTests(TestCase, QueryCountMixin):
    def setUp(self):
        # Create sample data
        skill = Skill.objects.create(name="AI")
        for i in range(10):
            course = Course.objects.create(course_name=f"Course {i}", institution="NTU")
            CourseSkill.objects.create(course=course, skill=skill, relevance=1.0)

    def test_courses_by_skills_query_efficiency(self):
        """Should execute in reasonable query count."""
        from rest_framework.test import APIClient
        client = APIClient()

        start = time.time()
        response = client.post("/api/courses/by-skills/", {"skills": ["AI"]}, format="json")
        duration = time.time() - start

        # Performance assertions
        self.assertEqual(response.status_code, 200)
        self.assertLess(duration, 0.5, "Query took too long (>0.5s)")
        self.assertLessEqual(len(connection.queries), 10, "Too many DB queries executed")

        # Sanity check
        self.assertTrue(len(response.data) > 0)


# ------------------------------------------
# /api/industries/<id>/context/
# ------------------------------------------
class IndustryContextPerformanceTests(TestCase, QueryCountMixin):
    def setUp(self):
        self.industry = Industry.objects.create(name="Finance")
        for i in range(5):
            Skill.objects.create(name=f"Skill {i}")
        for yr in range(2018, 2024):
            from skillsbridge_core.models import Metric
            Metric.objects.create(
                metric_type="employment_rate",
                value=80 + (yr - 2018),
                unit="%",
                dataset_vintage=yr,
                source_name="MOE",
                source_url="http://example.com",
                industry=self.industry
            )

    def test_industry_context_efficient_query(self):
        """IndustryService.context should retrieve data efficiently."""
        from rest_framework.test import APIClient
        client = APIClient()
        start = time.time()
        resp = client.get(f"/api/industries/{self.industry.id}/context/")
        duration = time.time() - start

        self.assertEqual(resp.status_code, 200)
        self.assertLess(duration, 0.5)
        self.assertNumQueriesLessThan(5)
        self.assertIn("metrics", resp.data)


# ------------------------------------------
# /api/bookmarks/
# ------------------------------------------
class BookmarkPerformanceTests(TestCase, QueryCountMixin):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        from rest_framework.test import APIClient
        self.client = APIClient()
        self.client.login(username="tester", password="12345")

        # Populate many bookmarks
        for i in range(10):
            course = Course.objects.create(course_name=f"Course {i}", institution="SP")
            Bookmark.objects.create(user=self.user, course=course)

    def test_bookmark_list_prefetches_courses(self):
        """Ensure BookmarkViewSet.list prefetches Course efficiently."""
        start = time.time()
        response = self.client.get("/api/bookmarks/")
        duration = time.time() - start

        self.assertEqual(response.status_code, 200)
        self.assertLess(duration, 0.5)
        self.assertNumQueriesLessThan(5)
        self.assertTrue(isinstance(response.data, list))
