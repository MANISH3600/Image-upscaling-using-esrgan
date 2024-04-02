from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'myapp'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
                import myapp.signals


