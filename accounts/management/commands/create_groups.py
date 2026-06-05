from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User
from students.models import Student, Group as StudentGroup
from courses.models import Discipline, Course, Topic
from assignments.models import Assignment, Submission
from staff.models import Teacher, Manager


class Command(BaseCommand):
    help = 'Создает группы teachers и managers с правами доступа'

    def handle(self, *args, **options):
        teachers_group, _ = Group.objects.get_or_create(name='teachers')
        managers_group, _ = Group.objects.get_or_create(name='managers')

        models = {
            'user': ContentType.objects.get_for_model(User),
            'student': ContentType.objects.get_for_model(Student),
            'group': ContentType.objects.get_for_model(StudentGroup),
            'discipline': ContentType.objects.get_for_model(Discipline),
            'course': ContentType.objects.get_for_model(Course),
            'topic': ContentType.objects.get_for_model(Topic),
            'assignment': ContentType.objects.get_for_model(Assignment),
            'submission': ContentType.objects.get_for_model(Submission),
            'teacher': ContentType.objects.get_for_model(Teacher),
            'manager': ContentType.objects.get_for_model(Manager),
        }

        # Права для менеджеров (все права)
        manager_permissions = []
        for ct in models.values():
            manager_permissions.extend(Permission.objects.filter(content_type=ct))
        managers_group.permissions.set(manager_permissions)
        self.stdout.write(self.style.SUCCESS(f'Добавлено {len(manager_permissions)} прав для managers'))

        # Права для преподавателей (только просмотр и изменение оценок)
        teacher_permissions = []
        view_permissions = ['view_course', 'view_topic', 'view_assignment', 'view_submission']
        for perm_codename in view_permissions:
            for ct in [models['course'], models['topic'], models['assignment'], models['submission']]:
                try:
                    perm = Permission.objects.get(codename=perm_codename, content_type=ct)
                    teacher_permissions.append(perm)
                except Permission.DoesNotExist:
                    pass
        
        # Право на изменение оценок
        try:
            change_perm = Permission.objects.get(codename='change_submission', content_type=models['submission'])
            teacher_permissions.append(change_perm)
        except Permission.DoesNotExist:
            pass
        
        teachers_group.permissions.set(teacher_permissions)
        self.stdout.write(self.style.SUCCESS(f'Добавлено {len(teacher_permissions)} прав для teachers'))

        for user in User.objects.filter(is_staff=True):
            if not Teacher.objects.filter(account=user).exists():
                user.groups.add(managers_group)
                self.stdout.write(f'Добавлен менеджер: {user.username}')

        # Преподаватели
        for teacher in Teacher.objects.all():
            teacher.account.groups.add(teachers_group)
            self.stdout.write(f'Добавлен преподаватель: {teacher.account.username}')

        self.stdout.write(self.style.SUCCESS('Группы и права успешно созданы!'))