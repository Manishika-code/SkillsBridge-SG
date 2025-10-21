from django.contrib import admin


from .models import Course, Skill, CourseSkill, Industry, Metric, SavedPlan, SavedPlanNode, Glossary, CourseIGP

admin.site.register(Course)
admin.site.register(Skill)
admin.site.register(CourseSkill)
admin.site.register(Industry)
admin.site.register(Metric)
admin.site.register(SavedPlan)
admin.site.register(SavedPlanNode)
admin.site.register(Glossary)
admin.site.register(CourseIGP)
