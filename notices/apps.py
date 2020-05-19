from django.apps import AppConfig


class NoticesConfig(AppConfig):
    name = 'notices'
    def ready(self):
        import notices.notice_signals
