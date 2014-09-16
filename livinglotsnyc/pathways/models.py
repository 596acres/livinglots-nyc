from caching.base import CachingQuerySet, CachingMixin
from feincms.models import Base

from livinglots_pathways.cms import PathwayFeinCMSMixin
from livinglots_pathways.models import BasePathway, BasePathwayManager


class PathwayManager(BasePathwayManager):

    def get_queryset(self):
        return CachingQuerySet(self.model, self._db)


class Pathway(CachingMixin, PathwayFeinCMSMixin, BasePathway, Base):
    objects = PathwayManager()
