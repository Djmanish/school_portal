from django.apps import AppConfig


class LibraryConfig(AppConfig):
    name = 'library'
    def ready(self):
        import library.library_signals
