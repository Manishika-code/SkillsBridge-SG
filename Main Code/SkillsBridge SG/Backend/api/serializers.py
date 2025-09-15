from rest_framework import serializers
from skillsbridge_core.models import (
    Course, Skill, Industry, Metric, SavedPlan, SavedPlanNode
)

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = "__all__"

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = "__all__"

class SavedPlanNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPlanNode
        fields = "__all__"

class SavedPlanSerializer(serializers.ModelSerializer):
    nodes = SavedPlanNodeSerializer(many=True, read_only=True)
    class Meta:
        model = SavedPlan
        fields = "__all__"