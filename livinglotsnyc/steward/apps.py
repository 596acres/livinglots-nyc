from django.apps import AppConfig

from actstream import registry


class StewardAppConfig(AppConfig):
    name = 'steward'

    def ready(self):
        registry.register(self.get_model('StewardNotification'))
        registry.register(self.get_model('StewardProject'))

        from .signals import *
