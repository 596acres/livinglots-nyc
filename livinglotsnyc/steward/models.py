from django.db import models
from django.utils.translation import ugettext_lazy as _

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
        return self.project_name or '%d' % self.pk


class StewardNotification(BaseStewardNotification):
    pass
