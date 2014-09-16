from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

import django_monitor

from livinglots_groundtruth.models import BaseGroundtruthRecord
from livinglots_notify.helpers import notify_facilitators


class GroundtruthRecord(BaseGroundtruthRecord):
    use = models.ForeignKey('livinglots_lots.Use',
        verbose_name=_('use'),
        limit_choices_to={'visible': False},
        blank=True,
        null=True,
    )


#
# Signals
#

@receiver(django_monitor.post_moderation, sender=GroundtruthRecord,
          dispatch_uid='groundtruth_groundtruthrecord_notify')
def notify(sender, instance=None, **kwargs):
    """
    Notify facilitators if the instance is pending.
    """
    if not instance and instance.is_pending:
        return
    notify_facilitators(instance)


@receiver(django_monitor.post_moderation, sender=GroundtruthRecord,
          dispatch_uid='groundtruth_groundtruthrecord')
def update_use(sender, instance, **kwargs):
    """
    Once a GroundtruthRecord is moderated and approved, make it official by
    updating the use on the referred-to Lot.
    """
    if not instance.is_approved or not instance.content_object:
        return

    lot = instance.content_object

    lot.known_use = instance.use
    lot.known_use_certainty = 10
    lot.known_use_locked = True
    lot.save()
