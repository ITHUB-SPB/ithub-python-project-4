from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Course, Topic
from assignments.models import Assignment, Answer
from itertools import chain
from django.db.models import Sum
from django.http import JsonResponse

class CourseListView(LoginRequiredMixin, ListView):
    template_name = "courses/course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        try:
            student = self.request.user.student
        except AttributeError:
            return Course.objects.none()
        if student.group:
            return Course.objects.filter(group=student.group).select_related("discipline", "teacher", "group")

        return Course.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            student = self.request.user.student
        except AttributeError:
            return context

        scores = Answer.objects.filter(
            student=student,
            score__isnull=False
        ).values("assignment__discipline").annotate(
            total_score=Sum("score")
        )
        scores_dict = {item["assignment__discipline"]: item["total_score"] for item in scores}

        for course in context["courses"]:
            course.total_score = scores_dict.get(course.discipline_id, 0)
            if course.total_score >= 90:
                course.grade = "5"
            elif course.total_score >= 70:
                course.grade = "4"
            elif course.total_score >= 50:
                course.grade = "3"
            else:
                course.grade = "2"

        sort = self.request.GET.get("sort", "")
        courses = list(context["courses"])
        if sort == "score_asc":
            courses.sort(key=lambda c: c.total_score)
        elif sort == "score_desc":
            courses.sort(key=lambda c: c.total_score, reverse=True)

        context["courses"] = courses
        context["current_sort"] = sort
        return context

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        if course.discipline:
            topics = list(course.discipline.topics.all())
            assignments = list(course.discipline.assignments.all())
            combined = sorted(
                chain(topics, assignments),
                key=lambda x: x.order
            )
            for item in combined:
                item.is_assignment = hasattr(item, "weight")
            context["items"] = combined
        else:
            context["items"] = []
        return context

class TopicDetailView(LoginRequiredMixin, DetailView):
    model = Topic
    template_name = "courses/topic_detail.html"
    context_object_name = "topic"


class AssignmentView(LoginRequiredMixin, View):
    template_name = "courses/assignment.html"

    def get(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        try:
            student = request.user.student
        except AttributeError:
            return redirect("accounts:login")
        answer = Answer.objects.filter(student=student, assignment=assignment).first()
        return render(request, self.template_name, {
            "assignment": assignment,
            "answer": answer,
        })

    def post(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        try:
            student = request.user.student
        except AttributeError:
            return redirect("accounts:login")
        value = request.POST.get("value", "").strip()
        if not value:
            messages.error(request, "ответ не может быть пустым")
            return redirect("courses:assignment", pk=pk)
        Answer.objects.update_or_create(
            student=student,
            assignment=assignment,
            defaults={"value": value}
        )
        messages.success(request, "ответ отправлен")
        return redirect("courses:assignment", pk=pk)


class CourseListAPIView(LoginRequiredMixin, View):
    def get(self, request):
        student = request.user.student
        sort = request.GET.get('sort', '')

        if student.group:
            courses = Course.objects.filter(group=student.group).select_related("discipline", "teacher", "group")
        else:
            courses = Course.objects.none()

        scores = Answer.objects.filter(
            student=student,
            score__isnull=False
        ).values("assignment__discipline").annotate(
            total_score=Sum("score")
        )
        scores_dict = {item["assignment__discipline"]: item["total_score"] for item in scores}

        data = []
        for course in courses:
            data.append({
                "id": course.pk,
                "discipline": course.discipline.title,
                "teacher": f"{course.teacher.surname} {course.teacher.name[0]}.",
                "group": course.group.title,
                "score": scores_dict.get(course.discipline_id, 0),
            })

        if sort == "score_asc":
            data.sort(key=lambda x: x["score"])
        elif sort == "score_desc":
            data.sort(key=lambda x: x["score"], reverse=True)

        return JsonResponse(data, safe=False)
