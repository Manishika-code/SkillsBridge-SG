from django.contrib import admin


from .models import Bookmark, Course, Skill, CourseSkill, Industry, Metric, SavedPlan, SavedPlanNode , CourseIGP

admin.site.register(Course)
admin.site.register(Skill)
admin.site.register(CourseSkill)
admin.site.register(Industry)
admin.site.register(Metric)
admin.site.register(SavedPlan)
admin.site.register(SavedPlanNode)
admin.site.register(CourseIGP)
admin.site.register(Bookmark)
