from django.db import models
from django.db.models import Q

from feincms.models import Base

from livinglots_pathways.cms import PathwayFeinCMSMixin
from livinglots_pathways.models import BasePathway, BasePathwayManager


class PathwayManager(BasePathwayManager):

    def get_for_lot(self, lot):
        pathways = super(PathwayManager, self).get_for_lot(lot)
        pathways = pathways.filter(Q(
            Q(borough=None) |
            Q(borough=lot.borough)
        ))
        return pathways


class Pathway(PathwayFeinCMSMixin, BasePathway, Base):
    objects = PathwayManager()

    BOROUGH_CHOICES = (
        ('Bronx', 'Bronx'),
        ('Brooklyn', 'Brooklyn'),
        ('Manhattan', 'Manhattan'),
        ('Queens', 'Queens'),
        ('Staten Island', 'Staten Island'),
    )
    borough = models.CharField(max_length=25, choices=BOROUGH_CHOICES,
                               blank=True, null=True)
