from django.db import models
from django.contrib.auth.models import User
import uuid

# this code describes entities

def uid(): return str(uuid.uuid4())

# selectable skills
class Skill(models.Model):
    id   = models.CharField(primary_key=True, max_length=36, default=uid, editable=False)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self): return self.name

# what courses are there (poly, jc, etc)
class Course(models.Model):
    LEVELS = [("poly","Polytechnic"),("jc","Junior College"),("uni","University")]
    id       = models.CharField(primary_key=True, max_length=36, default=uid, editable=False)
    level    = models.CharField(max_length=8, choices=LEVELS)
    name     = models.CharField(max_length=255)
    provider = models.CharField(max_length=64)
    skills   = models.ManyToManyField(Skill, through="CourseSkill")

    def __str__(self): return f"{self.name} ({self.provider})"

# courses in skillsfuture (not sure if we need this)
class CourseSkill(models.Model):
    course    = models.ForeignKey(Course, on_delete=models.CASCADE)
    skill     = models.ForeignKey(Skill, on_delete=models.CASCADE)
    relevance = models.FloatField(default=1.0)

    class Meta:
        unique_together = ("course", "skill")

# industry 
class Industry(models.Model):
    id   = models.CharField(primary_key=True, max_length=36, default=uid, editable=False)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self): return self.name

# metrics for certain courses and industry
class Metric(models.Model):
    METRIC_TYPES = [
        ("employment_rate", "Employment Rate"),
        ("median_salary", "Median Salary"),
        ("demand_growth", "Demand Growth"),
    ]
    id              = models.CharField(primary_key=True, max_length=36, default=uid, editable=False)
    metric_type     = models.CharField(max_length=32, choices=METRIC_TYPES)
    value           = models.FloatField()
    unit            = models.CharField(max_length=16, null=True, blank=True)
    dataset_vintage = models.IntegerField()
    source_name     = models.CharField(max_length=128)
    source_url      = models.URLField()
    course          = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    industry        = models.ForeignKey(Industry, null=True, blank=True, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)

# saves the plan to the user
class SavedPlan(models.Model):
    id        = models.CharField(primary_key=True, max_length=36, default=uid, editable=False)
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    name      = models.CharField(max_length=128)
    created_at= models.DateTimeField(auto_now_add=True)

# multiple plans 
class SavedPlanNode(models.Model):
    plan     = models.ForeignKey(SavedPlan, related_name="nodes", on_delete=models.CASCADE)
    node_type= models.CharField(max_length=16)  # "subject" | "course" | "role"
    ref_id   = models.CharField(max_length=36)
    order_idx= models.IntegerField()

# tba
class Glossary(models.Model):
    key   = models.CharField(primary_key=True, max_length=128)
    value = models.TextField()
