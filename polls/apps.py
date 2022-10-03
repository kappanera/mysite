from django.apps import AppConfig


class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    # add this
    def ready(self):
       import polls.signals  # noqa
