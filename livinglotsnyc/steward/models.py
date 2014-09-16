from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

import django_monitor

from livinglots_notify.helpers import notify_facilitators
from livinglots_steward.models import (BaseStewardProject,
                                       BaseStewardNotification)


class StewardProject(BaseStewardProject):

    organizer = models.ForeignKey('organize.Organizer',
        verbose_name=_('organizer'),
        blank=True,
        null=True,
        help_text=_('The organizer associated with this project.'),
    )
    external_id = models.CharField(_('external id'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('The external id for this project, if it is stored in '
                    'other databases'),
    )
    date_started = models.DateField(_('date started'),
        blank=True,
        null=True,
        help_text=_('When did this project start?'),
    )
    steward_notification = models.ForeignKey('StewardNotification',
        verbose_name=_('steward notification'),
        blank=True,
        null=True,
        help_text=_('The notification that led to the creation of this '
                    'project, if any.'),
    )

    def __unicode__(self):
        return self.name or '%d' % self.pk


class StewardNotification(BaseStewardNotification):
    pass


#
# Signals
#

@receiver(django_monitor.post_moderation, sender=StewardNotification,
          dispatch_uid='steward_stewardnotification_notify')
def notify(sender, instance=None, **kwargs):
    """
    Notify facilitators if the instance is pending.
    """
    if instance and instance.is_pending:
        notify_facilitators(instance)


@receiver(django_monitor.post_moderation, sender=StewardNotification,
          dispatch_uid='steward_stewardnotification')
def create_steward_project_and_organizer(sender, instance, **kwargs):
    """
    Once a StewardNotification is moderated and approved, make it official by
    creating an Organizer object and StewardProject as defined by the
    StewardNotification.
    """
    if not instance.is_approved:
        return

    # Create an organizer
    from organize.models import Organizer

    organizer = Organizer(
        content_type=instance.content_type,
        object_id=instance.object_id,
        name=instance.name,
        phone=instance.phone,
        email=instance.email,
        type=instance.type,
        url=instance.url,
        facebook_page=instance.facebook_page,
    )
    organizer.save()

    # Create a steward project
    steward_project = StewardProject(
        organizer=organizer,
        content_type=instance.content_type,
        object_id=instance.object_id,
        project_name=instance.project_name,
        use=instance.use,
        support_organization=instance.support_organization,
        land_tenure_status=instance.land_tenure_status,
        include_on_map=instance.include_on_map,
        steward_notification=instance,
    )
    steward_project.save()

    lot = steward_project.content_object
    lot.known_use = steward_project.use
    lot.known_use_certainty = 10
    lot.known_use_locked = True
    lot.steward_inclusion_opt_in = steward_project.include_on_map
    lot.save()
