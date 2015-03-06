from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from livinglots_organize.admin import BaseOrganizerAdmin

from lots.models import Lot
from .models import Organizer


class OrganizerAdmin(BaseOrganizerAdmin):

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(OrganizerAdmin, self) \
                .get_search_results(request, queryset, search_term)

        # Try to match by organized lot's name and BBL
        matching_lots = Lot.objects.filter(Q(bbl__contains=search_term) |
                                           Q(name__icontains=search_term))
        if matching_lots:
            queryset |= self.model.objects.filter(
                content_type=ContentType.objects.get_for_model(Lot),
                object_id__in=matching_lots.values_list('pk', flat=True),
            )
        return queryset, use_distinct


admin.site.register(Organizer, OrganizerAdmin)
