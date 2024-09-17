from django.apps import AppConfig


class ConfirmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'confirm_app'

    def ready(self) -> None:
        import confirm_app.signals