from django.apps import AppConfig


class FeesConfig(AppConfig):
    name = 'fees'
    def ready(self):
        import fees.fees_signals










