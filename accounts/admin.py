from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_groups(apps, schema_editor):
    teachers_group, _ = Group.objects.get_or_create(name='teachers')
    managers_group, _ = Group.objects.get_or_create(name='managers')
    
    Course = apps.get_model('courses', 'Course')
    Topic = apps.get_model('courses', 'Topic')
    Assignment = apps.get_model('assignments', 'Assignment')
    Submission = apps.get_model('assignments', 'Submission')
    Student = apps.get_model('students', 'Student')
    Teacher = apps.get_model('staff', 'Teacher')
    GroupModel = apps.get_model('students', 'Group')
    Discipline = apps.get_model('courses', 'Discipline')
    
    manager_perms = Permission.objects.filter(
        content_type__in=[
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(Topic),
            ContentType.objects.get_for_model(Assignment),
            ContentType.objects.get_for_model(Submission),
            ContentType.objects.get_for_model(Student),
            ContentType.objects.get_for_model(Teacher),
            ContentType.objects.get_for_model(GroupModel),
            ContentType.objects.get_for_model(Discipline),
        ]
    )
    managers_group.permissions.set(manager_perms)
    
    teacher_perms = Permission.objects.filter(
        codename__in=[
            'view_course', 'view_topic', 'view_assignment', 'view_submission', 'change_submission'
        ]
    )
    teachers_group.permissions.set(teacher_perms)

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('courses', '__first__'),
        ('assignments', '__first__'),
        ('students', '__first__'),
        ('staff', '__first__'),
    ]
    operations = [
        migrations.RunPython(create_groups),
    ]