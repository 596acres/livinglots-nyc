from django.db.models.signals import post_save
from django.dispatch import receiver

from newsletter.subscribe import subscribe
from .models import Organizer


@receiver(post_save, sender=Organizer, dispatch_uid='organize_subscribe_organizer')
def subscribe_organizer(sender, created=False, instance=None, **kwargs):
    if created:
        subscribe(instance, is_participating=True)
