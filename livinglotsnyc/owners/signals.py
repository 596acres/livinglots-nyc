from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Owner


@receiver(post_save, sender=Owner, dispatch_uid='owners_update_lots')
def update_lots(sender, created=False, instance=None, **kwargs):
    """
    Force a save on each lot the owner is associated with, moving each lot to
    a new layer accordingly.

    This is only really crucial for those situations where an owner moves from
    private to public or vice versa--the lots it controls show up on the wrong
    ownership type layer and things get confusing.
    """
    # This is too slow with owners that have many lots, so skip them
    if instance.lot_set.count() > 100:
        return
    for lot in instance.lot_set.all():
        lot.save()
