from django.apps import AppConfig


class AddchildConfig(AppConfig):
    name = 'AddChild'
    def ready(self):
        import AddChild.add_child_signal
