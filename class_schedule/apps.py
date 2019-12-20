from django.apps import AppConfig


class ClassScheduleConfig(AppConfig):
    name = 'class_schedule'
    def ready(self):
        import class_schedule.schedule_signal
