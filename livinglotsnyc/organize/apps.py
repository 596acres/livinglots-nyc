from django.apps import AppConfig

from actstream import registry


class OrganizeAppConfig(AppConfig):
    name = 'organize'

    def ready(self):
        registry.register(self.get_model('Organizer'))

        from .signals import *
