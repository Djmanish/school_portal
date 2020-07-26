from django.apps import AppConfig


class BusManagementConfig(AppConfig):
    name = 'bus_management'
    def ready(self):
        import bus_management.vehicle_signals