from django.contrib import admin


from .models import Bookmark, Career, Course, CourseCareer, CourseIntake, GESRecord, Skill, CourseSkill, Industry, Metric, SavedPlan, SavedPlanNode , CourseIGP, DiplomaToDegree

admin.site.register(Course)
admin.site.register(Skill)
admin.site.register(CourseSkill)
admin.site.register(Industry)
admin.site.register(Metric)
admin.site.register(SavedPlan)
admin.site.register(SavedPlanNode)
admin.site.register(CourseIGP)
admin.site.register(Bookmark)
admin.site.register(DiplomaToDegree)
admin.site.register(Career)
admin.site.register(CourseCareer)
admin.site.register(GESRecord)
admin.site.register(CourseIntake)
