from django.dispatch import receiver

import django_monitor

from livinglots_notify.helpers import notify_facilitators
from .models import StewardNotification, StewardProject


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
    lot.name = steward_project.project_name
    lot.steward_inclusion_opt_in = steward_project.include_on_map
    lot.save()
