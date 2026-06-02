from django.contrib import admin

from courses.models import Assignment, Course, Discipline, Submission, Topic


admin.site.register(Discipline)
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Assignment)
admin.site.register(Submission)
