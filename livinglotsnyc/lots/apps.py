from django.apps import AppConfig

from actstream import registry


class LotsAppConfig(AppConfig):
    name = 'lots'

    def ready(self):
        registry.register(self.get_model('Lot'))
