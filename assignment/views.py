from django.shortcuts import redirect, reverse
from assignment import models

def index(request, assignment_id):
    answer = request.POST.get('answer')

    models.Submission(
        student=request.user.student,
        assignment=models.Assignment.objects.get(pk=assignment_id),
        answer=answer
    ).save()

    return redirect(reverse('courses_list'))