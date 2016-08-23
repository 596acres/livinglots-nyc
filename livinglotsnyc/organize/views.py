from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from braces.views import JSONResponseMixin

from lots.models import Lot
from .models import Organizer


class OrganizersJSON(JSONResponseMixin, ListView):
    model = Organizer

    def check_request_allowed(self, request):
        key = request.GET.get('key', None)
        if key not in settings.LLNYC_API_KEYS:
            raise PermissionDenied

    def get_properties(self, organizer):
        organizer_dict = {
            'added': organizer.added,
            'email_hash': organizer.email_hash,
            'lot_pk': organizer.object_id,
            'name': organizer.name,
            'pk': organizer.pk,
            'public': organizer.post_publicly,
            'type': organizer.type.name,
        }
        try:
            organizer_dict['email'] = organizer.email
        except AttributeError:
            pass
        try:
            organizer_dict['notes'] = organizer.notes
        except AttributeError:
            pass
        try:
            organizer_dict['phone'] = organizer.phone
        except AttributeError:
            pass
        return organizer_dict

    def get_visible_lots_pks(self):
        """
        Get pks for visible lots--the lots that we export in VisibleLotsGeoJSON.
        """
        return Lot.visible.filter(
            lotgroup__isnull=True,
            centroid__isnull=False,
            polygon__isnull=False,
            gutterspace=False,
            owner__owner_type='public',
        ).exclude(
            owner__name='New York City Department of Parks & Recreation - building',
        ).values_list('pk', flat=True)

    def get_queryset(self):
        """Get only the organizers on visible lots."""
        qs = super(OrganizersJSON, self).get_queryset()
        return qs.filter(
            object_id__in=self.get_visible_lots_pks()
        ).select_related('type')

    def get_organizers_dicts(self):
        return [self.get_properties(o) for o in self.get_queryset()]

    def get(self, request, *args, **kwargs):
        self.check_request_allowed(request)

        context = {
            'organizers': self.get_organizers_dicts(),
        }
        return self.render_json_response(context)
