from django.apps import AppConfig


class TimetableAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'timetable_app'

    def ready(self):
        from django.contrib.auth.models import User

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'om',
                'omkumartiwari@gmail.com',
                'om123'
            )