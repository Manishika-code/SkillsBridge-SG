from rest_framework import serializers
from skillsbridge_core.models import (
    Course, Skill, Industry, Metric, SavedPlan, SavedPlanNode, Bookmark, DiplomaToDegree, Career, CourseCareer, CourseIGP
)

# using factory pattern to convert our django models to REST 

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

class BookmarkSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    class Meta: 
        model = Bookmark
        fields = "__all__"

    def get_course(self, obj):
        return CourseSerializer(obj.course).data

    
class DiplomaToDegreeSerializer(serializers.ModelSerializer):
    diploma = CourseSerializer(read_only=True)
    degree = CourseSerializer(read_only=True)

    class Meta:
        model = DiplomaToDegree
        fields = "__all__"


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = "__all__"


class CourseCareerSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    career = CareerSerializer(read_only=True)

    class Meta:
        model = CourseCareer
        fields = "__all__"
    def get_career(self, obj):
        return {
            "id": obj.career.id,
            "name": obj.career.name,
            "description": obj.career.description,
            "industry": obj.career.industry.name if obj.career.industry else None
        }

class CourseIGPSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseIGP
        fields = "__all__"
