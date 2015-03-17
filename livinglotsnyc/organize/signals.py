from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from lots.models import Lot
from newsletter.subscribe import subscribe_obj
from .models import Organizer


@receiver(post_save, sender=Organizer, dispatch_uid='organize_subscribe_organizer')
def subscribe_organizer(sender, created=False, instance=None, **kwargs):
    if created:
        subscribe_obj(instance, is_participating=True)


@receiver(post_save, sender=Organizer, dispatch_uid='organize_update_lot')
def update_lot(sender, created=False, instance=None, **kwargs):
    """
    Force a save on the organizer's target, which will move the lot to a new
    layer accordingly.
    """
    if created:
        instance.content_object.save()


@receiver(post_delete, sender=Organizer, dispatch_uid='organize_post_delete_update_lot')
def post_delete_update_lot(sender, instance=None, **kwargs):
    """
    Force a save on the organizer's target, which will remove the lot from
    layers accordingly.
    """
    if instance.content_object and Lot.objects.filter(pk=instance.content_object.pk).exists():
        instance.content_object.save()
