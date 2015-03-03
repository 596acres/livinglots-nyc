from django.apps import AppConfig

from actstream import registry


class OwnersAppConfig(AppConfig):
    name = 'owners'

    def ready(self):
        registry.register(self.get_model('Owner'))

        from .signals import *
