from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from .models import Skill

class SkillModelTest(TestCase):
    def test_create_skill(self):
        s = Skill.objects.create(name="AI")
        self.assertEqual(str(s), "AI")