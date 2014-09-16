# Add receivers for creating actions
from django.db.models.signals import post_save
from django.dispatch import receiver

from inplace_activity_stream.signals import action
from livinglots_usercontent.files.models import File
from livinglots_usercontent.notes.models import Note
from livinglots_usercontent.photos.models import Photo


def _add_action(sender, verb, created=False, instance=None, **kwargs):
    if not instance or not created: return
    action.send(
        sender,
        verb=verb,
        action_object=instance, # action object, what was created
        place=instance.content_object.centroid, # where did it happen?
        target=instance.content_object, # what did it happen to?
        data={},
    )


@receiver(post_save, sender=Note, dispatch_uid='activity_stream.note')
def add_note_action(sender, instance=None, **kwargs):
    if not instance: return
    _add_action(instance.added_by, 'wrote', instance=instance, **kwargs)


@receiver(post_save, sender=Photo, dispatch_uid='activity_stream.photo')
def add_photo_action(sender, instance=None, **kwargs):
    if not instance: return
    _add_action(instance.added_by, 'posted a picture', instance=instance,
                **kwargs)


@receiver(post_save, sender=File, dispatch_uid='activity_stream.file')
def add_file_action(sender, instance=None, **kwargs):
    if not instance: return
    _add_action(instance.added_by, 'posted a file', instance=instance,
                **kwargs)
