from django.apps import AppConfig


class StaffConfig(AppConfig):
    name = "staff"
    verbose_name = "Сотрудники"

    def ready(self):
        import staff.signals
