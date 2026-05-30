from django.contrib import admin
from courses import models


class DiscliplineAdmin(admin.ModelAdmin):
	list_display = ['title', 'duration']
	list_filter = ['duration']
	search_fields = ['title']


class CourseAdmin(admin.ModelAdmin):
	list_display = ['discipline', 'group__title', 'teacher']
	list_filter = ['group', 'teacher']
	search_fields = ['discipline__title']

	def get_queryset(self, request):
		if request.user.groups.filter(name='teachers').exists():
			return super().get_queryset(request).filter(teacher=request.user.teacher)
		return super().get_queryset(request)


class TopicAdmin(admin.ModelAdmin):
	list_display = ['discipline', 'title']
	list_filter = ['discipline']
	search_fields = ['title']


class AssignmentAdmin(admin.ModelAdmin):
	list_display = ['topic__discipline__title', 'topic__title', 'weight']
	list_filter = ['topic__discipline']
	search_fields = ['topic__title']


class SubmissionAdmin(admin.ModelAdmin):
	list_display = ['assignment__topic__discipline__title', 'assignment__topic__title',
	                'student', 'score']
	list_filter = ['assignment__topic__discipline']
	search_fields = ['topic__title']

	readonly_fields = ['student', 'assignment', 'answer']


admin.site.register(models.Discipline, DiscliplineAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Assignment, AssignmentAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Submission, SubmissionAdmin)